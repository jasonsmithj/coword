$(function() {
  $('#process').click(function() {
    $.blockUI({
      message: 'In Processing',
      css: {
        border: 'none',
        padding: '10px',
        backgroundColor: '#333',
        opacity: .5,
        color: '#fff'
      },
      overlayCSS: {
        backgroundColor: '#000',
        opacity: 0.6
      }
    });
  });
});
