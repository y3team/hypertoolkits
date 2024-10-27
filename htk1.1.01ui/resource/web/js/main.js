    // Function to scroll to the top of the page
    function scrollToTop() {
        window.scrollTo({
          top: 0,
          behavior: 'smooth'
        });
      }
  
      // Show or hide the back-to-top button based on scroll position
      window.addEventListener('scroll', function() {
        var backToTopButton = document.querySelector('.back-to-top');
        if (window.scrollY > 100) {
          backToTopButton.style.display = 'block';
        } else {
          backToTopButton.style.display = 'none';
        }
      });
      
