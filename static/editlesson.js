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
      const songButton = document.createElement("a");
      // link.href = song.url; url is removed and replaced by songId
      songButton.onclick = function() { selectsong(songButton); };
      songButton.textContent = song.name;
      songButton.id = song.songId
      dropdown.appendChild(songButton);
    });

    dropdown.classList.add("show");

    // now that links exist, run your filter
    filterFunction();

  } catch (err) {
    console.error("Error fetching songs:", err);
  }
}

async function selectsong(song) {
  // Elements
  const titleSpan = document.getElementById("selectedSongTitle");
  const bpmSpan = document.getElementById("selectedSongBpm");
  const energySpan = document.getElementById("selectedSongEnergy");
  const durationSpan = document.getElementById("selectedSongDuration");
  const cover = document.getElementById("selectedSongImage");

  // Optional: clear out old data while loading
  titleSpan.textContent = "Loading...";
  bpmSpan.textContent = "";
  energySpan.textContent = "";
  durationSpan.textContent = "";
  cover.src = "";

  try {
    // Fetch detailed song data from your Flask backend
    const response = await fetch(`/get_song_data?q=${encodeURIComponent(song.id)}`);
    if (!response.ok) throw new Error("Failed to load song data");

    const data = await response.json();

    // Update the UI
    titleSpan.textContent = `${data.name} — ${data.artists.join(", ")}`;
    bpmSpan.textContent = data.bpm ? `${data.bpm} BPM` : "N/A";
    energySpan.textContent = data.energy !== null ? `${Math.round(data.energy * 100)}% energy` : "N/A";
    durationSpan.textContent = data.duration_min ? `${data.duration_min} min` : "N/A";
    cover.src = data.album_cover || "";

  } catch (err) {
    console.error(err);
    titleSpan.textContent = "Error loading song data";
    bpmSpan.textContent = "";
    energySpan.textContent = "";
    durationSpan.textContent = "";
    cover.src = "";
  }
}

//piechart
function piechart(data) {
var canvas = document.getElementById("energychart"); 
var ctx = canvas.getContext("2d"); 
var lastend = 0; 
var myTotal = 0;
var myColor = ['#afcc4c', '#95b524','#c1dd54', '#9cb83d'];
var labels = ['A', 'B', 'C', 'D'];

for(var e = 0; e < data.length; e++)
{
  myTotal += data[e];
}

// make the chart 10 px smaller to fit on canvas
var off = 10
var w = (canvas.width - off) / 2
var h = (canvas.height - off) / 2
for (var i = 0; i < data.length; i++) {
  ctx.fillStyle = myColor[i];
  ctx.strokeStyle ='white';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(w,h);
  var len =  (data[i]/myTotal) * 2 * Math.PI
  var r = h - off / 2
  ctx.arc(w , h, r, lastend,lastend + len,false);
  ctx.lineTo(w,h);
  ctx.fill();
  ctx.stroke();
  ctx.fillStyle ='white';
  ctx.font = "20px Arial";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  var mid = lastend + len / 2
  ctx.fillText(labels[i],w + Math.cos(mid) * (r/2) , h + Math.sin(mid) * (r/2));
  lastend += Math.PI*2*(data[i]/myTotal);
}
}; 