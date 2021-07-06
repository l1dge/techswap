function displayShowPop() {
    document.getElementById("popular").style.visibility = "visible";
    document.getElementById("popular").style.display = "block";
    document.getElementById("latest").style.visibility = "hidden";
    document.getElementById("latest").style.display = "none";
    document.getElementById("category").style.visibility = "hidden";
    document.getElementById("category").style.display = "none";
}


function displayShowLatest() {
    document.getElementById("latest").style.visibility = "visible";
    document.getElementById("latest").style.display = "block";
    document.getElementById("category").style.visibility = "hidden";
    document.getElementById("popular").style.visibility = "hidden"; 
    document.getElementById("category").style.display = "none";
    document.getElementById("popular").style.display = "none";
}

function displayShowCat() {
document.getElementById("category").style.visibility = "visible";
document.getElementById("category").style.display = "block";
document.getElementById("latest").style.visibility = "hidden";
document.getElementById("popular").style.visibility = "hidden";
document.getElementById("latest").style.display = "none";
document.getElementById("popular").style.display = "none";
}
