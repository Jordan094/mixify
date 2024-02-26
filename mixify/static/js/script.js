// Materialise CSS Navbar
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOMContentLoaded event fired');
    
    var elems = document.querySelectorAll('.sidenav');
    console.log('Found elements:', elems);
    
    var instances = M.Sidenav.init(elems);
    console.log('Sidenav instances:', instances);
  });
  
// Function to Validate user is 18 Credit to https://www.javatpoint.com/ for guidance
  function validateAge() {
    var dobInput = document.getElementById('dob');
    var dobValue = dobInput.value;

    var dobDate = new Date(dobValue);
    var currentDate = new Date();
    var age = currentDate.getFullYear() - dobDate.getFullYear() - 1;

    if (currentDate.getMonth() > dobDate.getMonth() ||
        (currentDate.getMonth() === dobDate.getMonth() && currentDate.getDate() >= dobDate.getDate())) {
        age++;
    }

    if (age < 18) {
        alert('You must be 18 or older to sign up.');
        return false;
    }

    return true;
}


