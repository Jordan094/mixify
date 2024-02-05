document.addEventListener('DOMContentLoaded', function() {
    console.log('DOMContentLoaded event fired');
    
    var elems = document.querySelectorAll('.sidenav');
    console.log('Found elements:', elems);
    
    var instances = M.Sidenav.init(elems);
    console.log('Sidenav instances:', instances);
  });
  

  