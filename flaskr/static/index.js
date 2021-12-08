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

$('#updateusermodal').on('show.bs.modal', function (event) {
  console.log('modalaufgerufen')
  var button = $(event.relatedTarget)
  console.log(button)
  var userid = button.data('userid')
  var username = button.data('username')
  var firstname = button.data('firstname')
  var name = button.data('name')
  var password = button.data('password')
  var isadmin = button.data('isadmin')
  
  $(this).find('#updateuserbutton').attr('onclick', `updateUser(${userid})`)
  $(this).find('#updateusername').val(username)
  $(this).find('#updatefirstname').val(firstname) 
  $(this).find('#updatename').val(name)
  $(this).find('#updatepassword').val(password) 
  console.log($(this).find('#updateisadmin').val)
  $(this).find('#updateisadmin').val(isadmin)
  document.getElementById('updateisadmin').checked = isadmin;
})

$('#newFilmModal').on('show.bs.modal', function (event) {
  console.log('modalaufgerufen')
  var button = $(event.relatedTarget)
  console.log(button)
  
  $(this).find('#newFilmButton').attr('onclick', `newFilm()`)
})


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

$('#updatefilmmodal').on('show.bs.modal', function (event) {
  console.log('modalaufgerufen')
  var button = $(event.relatedTarget)
  console.log(button)
  var filmid = button.data('filmid')
  var name = button.data('name')
  var description = button.data('description')
  var roomname = button.data('roomname')

  $(this).find('#updatefilmbutton').attr('onclick', `updateFilm(${filmid})`)
  $(this).find('#updatename').val(name)
  $(this).find('#updatedescription').val(description) 
  $(this).find('#updateroomname').val(roomname)
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


/* function updatefilmmodal(filmid) {

  const name = document.getElementById('name').value
  const description = document.getElementById('description').value
  const roomname = document.getElementById('roomname').value

    fetch("/admin/film/", {
    method: "UPDATE",
    body: JSON.stringify({ filmid: filmid, name: name,description:description,roomname:roomname}),
  }).then((_res) => {
    window.location.href = "/admin/film/";
  });
} 
 */

function newroom() {
    const newname = document.getElementById('newroomname').value
    console.log(newname)

    fetch("/admin/newroom", {
        method: "POST",
        body: JSON.stringify({newname: newname})
    }).then((_res) =>{
        window.location.href = "/rooms"
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

    console.log(formData)

    /* for (let value of formData.values()) {
        console.log(name,value); 
     }
    
     for (let value of formData.entries()) {
        console.log ("entries " + value[0] + " mit " + value[1]);
     } */

     fetch(`/admin/${roomid}/register/`,{
         method: "POST",
         body: formData
     }).then((_res) =>{
      window.location.href = `/danke`
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


function deleteUser(userid) {
  fetch('/admin/user/', {
      method: "DELETE",
      body: JSON.stringify({ userid: userid})
  }).then((_res)=> {
      window.location.href = "/admin/user/"
  });
}

function updateUser(userid) {
  const updateusername = document.getElementById('updateusername').value
  const updatefirstname = document.getElementById('updatefirstname').value
  const updatename = document.getElementById('updatename').value
  const updatepassword = document.getElementById('updatepassword').value
  const updateisadmin = document.getElementById('updateisadmin').checked
  console.log(userid,updateusername,updatefirstname,updatename,updatepassword,updateisadmin)

  fetch("/admin/user/", {
    method: "UPDATE",
    body: JSON.stringify({ userid:userid, updateusername:updateusername,updatefirstname:updatefirstname,updatename:updatename,updatepassword:updatepassword,updateisadmin:updateisadmin}),
  }).then((_res) => {
    window.location.href = "/admin/user/";
  });
}

function newUser() {
  console.log('test')
 const username = document.getElementById('username').value
  const firstname = document.getElementById('firstname').value
  const name = document.getElementById('name').value
  const password = document.getElementById('password').value
  const isadmin = document.getElementById('isadmin').checked
  console.log(username,firstname,name,password,isadmin)

  fetch("/admin/user/", {
      method: "POST",
      body: JSON.stringify({username: username,firstname:firstname,name:name,password:password,isadmin:isadmin})
  }).then((_res) =>{
      window.location.href = "/admin/user/"
  })
}

  

function newFilm(){
  const name = document.getElementById('name').value
  const description = document.getElementById('description').value
  const roomname = document.getElementById('roomname').value

  fetch('/admin/film/',{
    method: 'POST',
    body: JSON.stringify({name:name, description:description, roomname:roomname})
  }).then((_res)=>{
    window.location.href = "/admin/film/"
  })
}


function deleteFilm(filmid,roomid) {
  fetch('/admin/film/', {
      method: "DELETE",
      body: JSON.stringify({filmid: filmid, roomid:roomid})
  }).then((_res)=> {
      window.location.href = "/admin/film/"
  });
}

function updateFilm(filmid) {
  const name = document.getElementById('updatename').value
  const description = document.getElementById('updatedescription').value
  const roomname = document.getElementById('updateroomname').value

  fetch("/admin/film/", {
    method: "UPDATE",
    body: JSON.stringify({ filmid:filmid, name:name,description:description,roomname:roomname}),
  }).then((_res) => {
    window.location.href = "/admin/film/";
  });
}