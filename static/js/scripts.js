//Messages Functions
function WarningUndoItemDel(){
    if(confirm("Sure you want to delete? This will delete your item and cannot be undone!")){
      return true;
    } else {
      return false;
    }
  }

  function WarningUndoItemArc(){
    if(confirm("Sure you want to archive?")){
      return true;
    } else {
      return false;
    }
  }

//Shadow Function
$(document).ready(function() {
// executes when HTML-Document is loaded and DOM is ready
console.log("document is ready");


$( ".card" ).hover(
function() {
    $(this).addClass('shadow-lg p-2 rounded').css('cursor', 'pointer'); 
}, function() {
    $(this).removeClass('shadow-lg p-2 rounded');
}
);

// document ready  
});

//Places Lookup
function activatePlacesSearch(){
    var input = document.getElementById('citysearch');
    var autocomplete = new google.maps.places.Autocomplete(input);
}


//Homee Page Content Sorting
function displayShowAll() {
  document.getElementById("allitems").style.display = "block";
  document.getElementById("allitems").style.visibility = "visible";
  document.getElementById("category").style.display = "none";
  document.getElementById("category").style.visibility = "hidden";
  document.getElementById("latest").style.display = "none";
  document.getElementById("latest").style.visibility = "hidden";
  document.getElementById("popular").style.display = "none";
  document.getElementById("popular").style.visibility = "hidden";
}

function displayShowPop() {
  document.getElementById("popular").style.display = "block";
  document.getElementById("popular").style.visibility = "visible";
  document.getElementById("latest").style.display = "none";
  document.getElementById("latest").style.visibility = "hidden";
  document.getElementById("category").style.display = "none";
  document.getElementById("category").style.visibility = "hidden";
  document.getElementById("allitems").style.display = "none";
  document.getElementById("allitems").style.visibility = "hidden";
}


function displayShowLatest() {
  document.getElementById("latest").style.display = "block";
  document.getElementById("latest").style.visibility = "visible";
  document.getElementById("category").style.display = "none";
  document.getElementById("category").style.visibility = "hidden";
  document.getElementById("popular").style.display = "none";
  document.getElementById("popular").style.visibility = "hidden"; 
  document.getElementById("allitems").style.display = "none";
  document.getElementById("allitems").style.visibility = "hidden";
}

function displayShowCat() {
  document.getElementById("category").style.display = "block";
  document.getElementById("category").style.visibility = "visible";
  document.getElementById("latest").style.display = "none";
  document.getElementById("latest").style.visibility = "hidden";
  document.getElementById("popular").style.display = "none";
  document.getElementById("popular").style.visibility = "hidden";
  document.getElementById("allitems").style.display = "none";
  document.getElementById("allitems").style.visibility = "hidden";
}



//Button to go back to top
$(document).ready(function() {
    // executes when HTML-Document is loaded and DOM is ready
    console.log("document is ready");
  
  //Get the button
  let mybtn = document.getElementById("btn-back-to-top");
  
  // When the user scrolls down 20px from the top of the document, show the button
  window.onscroll = function () {
    scrollFunction();
  };
  
  function scrollFunction() {
    if (
      document.body.scrollTop > 20 ||
      document.documentElement.scrollTop > 20
    ) {
      mybtn.style.display = "block";
    } else {
      mybtn.style.display = "none";
    }
  }
  // When the user clicks on the button, scroll to the top of the document
  mybtn.addEventListener("click", backToTop);
  
  function backToTop() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
  }
  
  // document ready  
});