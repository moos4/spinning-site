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

async function fetchSongs() {
  const input = document.getElementById("searchsonginput");
  const query = input.value.trim();
  const dropdown = document.getElementById("songdropdown");

  // if the user deletes everything, clear list
  if (!query) {
    dropdown.innerHTML = "";
    dropdown.classList.remove("show");
    return;
  }

  try {
    // get songs from Flask
    const response = await fetch(`/search_songs?q=${encodeURIComponent(query)}`);
    const songs = await response.json();

    dropdown.innerHTML = "";

    if (songs.length === 0) {
      dropdown.innerHTML = "<a>No results found</a>";
      dropdown.classList.add("show");
      return;
    }

    // dynamically add songs to dropdown
    songs.forEach(song => {
      const link = document.createElement("a");
      link.href = song.url;
      link.textContent = song.name;
      link.target = "_blank";
      dropdown.appendChild(link);
    });

    dropdown.classList.add("show");

    // now that links exist, run your filter
    filterFunction();

  } catch (err) {
    console.error("Error fetching songs:", err);
  }
}
