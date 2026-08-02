
document.addEventListener('DOMContentLoaded',function(){
  var b=document.querySelector('.burger'),m=document.querySelector('.menu');
  if(b){b.addEventListener('click',function(){m.classList.toggle('open');});}
  document.querySelectorAll('.menu a').forEach(function(a){a.addEventListener('click',function(){m.classList.remove('open');});});
  var f=document.querySelector('form[data-enquiry]');
  if(f){f.addEventListener('submit',function(e){
    var ok=f.checkValidity();
    if(!ok)return;
  });}
});
