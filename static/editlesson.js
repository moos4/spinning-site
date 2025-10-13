function openaddsong_gui() { document.getElementById("addsong_gui").style.visibility = "visible"; }
function closeaddsong_gui() { document.getElementById("addsong_gui").style.visibility = "hidden"; }

function showlist() {
  document.getElementById("songdropdown").classList.toggle("show");
}

function filterFunction() {
  const input = document.getElementById("searchsonginput");
  const filter = input.value.toUpperCase();
  const div = document.getElementById("songdropdown");
  const a = div.getElementsByTagName("a");
  for (let i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}