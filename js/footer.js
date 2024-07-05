// footer.js
document.addEventListener("DOMContentLoaded", function() {
    const footerContent = `
        <div id="fh5co-footer" role="contentinfo">
            <div class="container">
                <div class="row d-flex justify-content-around">
                    <div class="col-md-5 animate-box footer-col">
                        <h3 class="section-title">Savior Sailor</h3>
                        <p>Savior Sailor has got your back whether it is your first OR last time leaving home.
                            Thank you for your service and support!</p>
                    </div>

                    <div class="col-md-5 animate-box footer-col">
                        <h3 class="section-title">Connect with Us</h3>
                        
                        <ul class="contact-info">
                            <li><i class="icon-envelope"></i><a href="#">saviorsailor75@gmail.com</a></li>
                            <li><i class="icon-globe"></i><a href="#">www.saviorsailor.com</a></li>
                        </ul>
                        <ul class="social-media">
                            <li><a href="https://www.facebook.com/profile.php?id=100075436362467" class="facebook" target="_blank"><i class="icon-facebook"></i></a></li>
                            <li><a href="https://www.instagram.com/savior.sailor/" class="instagram"><i class="icon-instagram" target="_blank"></i></a></li>
                            <li><a href="https://www.youtube.com/channel/UCyII3UTiO0U8al3tDQ8OHOA" class="instagram" target="_blank"><i class="icon-youtube-play"></i></a></li>
                        </ul>
                        <a href="https://calendly.com/spr3adsh33t/sponsor-a-sailor" class="btn btn-primary ml-2" target="_blank" style="height: 40px;">Chat with Alex</a>
                        <a href="https://forms.google.com" class="btn btn-primary ml-2" target="_blank" style="height: 40px;">Become a Sponsored Sailor</a>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        <p class="copy-right">&copy; 2024 Savior Sailor. All Rights Reserved.</p>
                    </div>
                </div>
            </div>
        </div>
    `;
    document.getElementById('footer-placeholder').innerHTML = footerContent;
});
