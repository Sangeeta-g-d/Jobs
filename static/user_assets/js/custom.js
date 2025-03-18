// script start to show more or less in the jobs page
document.addEventListener("DOMContentLoaded", function() {
    const viewMoreButtons = document.querySelectorAll(".view-more-btn");

    viewMoreButtons.forEach(button => {
        button.addEventListener("click", function() {
            let jobId = this.getAttribute("data-job-id");
            let detailsDiv = document.getElementById("job-details-" + jobId);
            let jobCard = this.closest(".single_jobs"); // Get the job card to scroll to

            // Close all other job details sections
            document.querySelectorAll(".job_details").forEach(div => {
                if (div !== detailsDiv) {
                    div.style.display = "none"; // Hide other job details
                }
            });

            // Reset all "View More" button texts
            document.querySelectorAll(".view-more-btn").forEach(btn => {
                if (btn !== this) {
                    btn.innerText = "View More";
                }
            });

            // Toggle the clicked job details section
            if (detailsDiv.style.display === "none" || detailsDiv.style.display === "") {
                detailsDiv.style.display = "block";  // Show details
                this.innerText = "View Less";  // Change button text
                
                // Smoothly scroll to the job card
                jobCard.scrollIntoView({ behavior: "smooth", block: "start" });
            } else {
                detailsDiv.style.display = "none";  // Hide details
                this.innerText = "View More";  // Reset button text
            }
        });
    });
});

// end of the show more or less in jobs


// script for job search --start
$(document).ready(function() {
    $("#search_designation").on("keyup", function() {
        var designation = $(this).val().trim();

        $.ajax({
            url: "{% url 'jobs' %}",
            type: "GET",
            data: {
                designation: designation
            },
            headers: {
                "X-Requested-With": "XMLHttpRequest"  // Required for detecting AJAX in Django
            },
            success: function(response) {
                var jobsList = $(".job_lists .row");
                jobsList.empty(); // Clear existing jobs

                if (response.jobs.length > 0) {
                    response.jobs.forEach(function(job) {
                        var jobHtml = `
                            <div class="col-lg-12 col-md-12">
                                <div class="single_jobs white-bg d-flex justify-content-between">
                                    <div class="jobs_left d-flex align-items-center">
                                        <div class="thumb">
                                            <img src="${job.company_logo}" alt="">
                                        </div>
                                        <div class="jobs_conetent">
                                            <a href="#"><h4>${job.job_title}</h4></a>
                                            <div class="links_locat d-flex align-items-center">
                                                <div class="location">
                                                    <p><i class="fa fa-map-marker"></i> ${job.location}</p>
                                                </div>
                                                <div class="location">
                                                    <p><i class="fa fa-clock-o"></i> ${job.job_type}</p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="jobs_right">
                                        <div class="apply_now">
                                            <a class="heart_mark" href="#"><i class="fa fa-heart"></i></a>
                                            <a href="/login" target="_blank" class="boxed-btn3">Apply Now</a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        `;
                        jobsList.append(jobHtml);
                    });
                } else {
                    jobsList.html("<p>No jobs found.</p>");
                }
            }
        });
    });
});
// end of the job search script

// contact form script alert start
document.getElementById("contactForm").addEventListener("submit", function (event) {
    event.preventDefault();
    let formData = new FormData(this);

    fetch("", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        Swal.fire({
            icon: 'success',
            title: 'Success!',
            text: data.message,
            showConfirmButton: false,
            timer: 2000
        });
        this.reset();
    })
    .catch(error => {
        Swal.fire({
            icon: 'error',
            title: 'Oops!',
            text: 'Something went wrong!'
        });
    });
});
// alert end