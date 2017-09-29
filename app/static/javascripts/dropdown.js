$(function(){
  $('.dropdown-menu a').click(function(){
    var visibleTag = $(this).parents('ul').attr('visibleTag');
    var hiddenTag = $(this).parents('ul').attr('hiddenTag');
    $(visibleTag).html($(this).attr('value'));
    $(hiddenTag).val($(this).attr('value'));
  })
})
