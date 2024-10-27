
document.addEventListener('DOMContentLoaded', function() {
  // Check localStorage for agreement status
  var agreementCheckup = localStorage.getItem('agreementcheckup');

  // If agreementcheckup is not set or is '0', show the agreement popup
  if (!agreementCheckup || agreementCheckup === '0') {
    // Display SweetAlert modal with Markdown content
    Swal.fire({
      title: 'User Agreement',
      html: `<div style="max-height: 400px; overflow-y: auto;">${fetchMarkdownContent('agreement.md')}</div>`,
      confirmButtonText: 'Confirm',
      allowOutsideClick: false,
      allowEscapeKey: false,
      showCancelButton: false,
      showCloseButton: true,
      didClose: () => {
        // Update localStorage after user closes the popup
        localStorage.setItem('agreementcheckup', '1');
      }
    });
  }
});

// Function to fetch Markdown content
function fetchMarkdownContent(url) {
  // Here you can fetch your Markdown content from a file or an endpoint
  // For simplicity, this example assumes you have a static Markdown file
  // Replace this with your actual fetching logic
  return `
# User Agreement

This is the user agreement content. Please read carefully and agree to proceed.

[ ] I have read and agree to the terms above.
`;
}
