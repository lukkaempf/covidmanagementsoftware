function deleteNote(noteId) {
    fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }

function deleteRoom(roomid) {
    fetch('/admin/deleteroom', {
        method: "POST",
        body: JSON.stringify({ roomid: roomid})
    }).then((_res)=> {
        window.location.href = "/admin"
    });
}


$('#exampleModal').on('show.bs.modal', function (event) {
    console.log('modalaufgerufen')
    var button = $(event.relatedTarget)
    console.log(button)
    var roomid = button.data('roomid')
    var oldname = button.data('oldname')
    console.log(oldname)
    $(this).find('#b1').attr('onclick', `updateRoomname(${roomid})`)
    $(this).find('#recipient-name').val(oldname)
    $(this).find('#b1').select()
    var input = document.getElementById('recipient-name');
    input.focus()
    input.select()
})

function updateRoomname(roomid) {

    const newname = document.getElementById('recipient-name').value
    console.log(newname)

    fetch("/admin/updateroomname", {
      method: "POST",
      body: JSON.stringify({ roomid: roomid, newname: newname}),
    }).then((_res) => {
      window.location.href = "/admin";
    });
  }


function newroom() {
    const newname = document.getElementById('newroomname').value
    console.log(newname)

    fetch("/admin/newroom", {
        method: "POST",
        body: JSON.stringify({newname: newname})
    }).then((_res) =>{
        window.location.href = "/admin"
    })
}

function registerseat(roomid) {
    const register = document.getElementById('registerseatinput')
    
    var formData = new FormData()
    formData.append('roomid', roomid)
    formData.append('vorname', register.vorname.value)
    formData.append('name', register.name.value)
    formData.append('klasse', register.klasse.value)
    formData.append('email', register.email.value)
    formData.append('sitzplatznumber', register.sitzplatznumber.value)

    /* for (let value of formData.values()) {
        console.log(name,value); 
     }
    
     for (let value of formData.entries()) {
        console.log ("entries " + value[0] + " mit " + value[1]);
     } */

     fetch(`/admin/${roomid}/register`,{
         method: "POST",
         body: formData
     }).then((_res) =>{
      window.location.href = `/admin/${roomid}/taken`
  })
}


/*Roomoptions QRcode gross anzeigen */
// Get the modal
var modal = document.getElementById("qrcode_modal");

// Get the image and insert it inside the modal - use its "alt" text as a caption
var img = document.getElementById("qrcode");
var modalImg = document.getElementById("img01");
img.onclick = function(){
  modal.style.display = "block";
  modalImg.src = this.src;
}

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("qrcode_modal_close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() { 
  modal.style.display = "none";
}


//Raumoptionen Qrcode drucken
const buttons = document.getElementById("print");

function function_print() {
  if (window.print) {
    window.print();
  }
}

buttons.addEventListener("click", function_print);

