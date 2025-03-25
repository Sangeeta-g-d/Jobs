
// pop up for adding job details
function openJobPopup(jobId) {
    fetch(`/get_job_details/${jobId}/`)
        .then(response => response.json())
        .then(data => {
            const content = `
                <p><strong>Job Title:</strong> ${data.job_title}</p>
                <p><strong>Company Name:</strong> ${data.company_name}</p>
                <p><strong>Salary:</strong> ${data.salary}</p>
                <p><strong>Experience:</strong> ${data.experience}</p>
                <p><strong>Location:</strong> ${data.location}</p>
                <p><strong>Education:</strong> ${data.education}</p>
                <p><strong>Job Type:</strong> ${data.job_type}</p>
                <p><strong>Work Mode:</strong> ${data.work_mode}</p>
                <p><strong>Skills:</strong> ${data.required_skills}</p>
                <p><strong>Roles and Responsibilities:</strong> ${data.roles_and_responsibilities}</p>
                <p><strong>Job Link:</strong> <a href="${data.job_link}" target="_blank">${data.job_link}</a></p>
            `;
            document.getElementById('jobDetailsContent').innerHTML = content;

            // Initialize the modal after content is updated
            const jobDetailsModal = new bootstrap.Modal(document.getElementById('jobDetailsModal'));
            jobDetailsModal.show();
        })
        .catch(error => {
            console.error('Error fetching job details:', error);
            alert('Failed to load job details. Please try again.');
        });
}


function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}
// pop up for deleting job details
function confirmDelete(jobId) {
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Delete',
        cancelButtonText: 'Cancel'
    }).then((result) => {
        if (result.isConfirmed) {
            // Send AJAX request to delete the record
            deleteJob(jobId);
        }
    });
}

function deleteJob(jobId) {
    const csrfToken = getCSRFToken();

    fetch(`/delete_job/${jobId}/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (response.ok) {
            Swal.fire('Deleted!', 'The job has been deleted.', 'success').then(() => {
                // Reload the page after clicking OK
                window.location.reload();
            });
        } else {
            Swal.fire('Error!', 'Unable to delete the job.', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        Swal.fire('Error!', 'Something went wrong.', 'error');
    });
}