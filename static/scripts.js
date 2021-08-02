function loadFile(event) {
	var video = document.getElementById('output');
	video.src = URL.createObjectURL(event.target.files[0]);
};

function selectedVid(self) {
  var file = self.files[0];
  var reader = new FileReader();

  reader.onload = function(e) {
    var src = e.target.result
    var video = document.getElementById("video");
    var source = document.getElementById("source");

    source.setAttribute("src", src);
    video.load()
    video.play()
  };

  reader.readAsDataURL(file)
}

function checkForm(form)
{
  if(!form.terms.checked) {
    alert("Please indicate that you accept the Terms and Conditions");
    form.terms.focus();
    return false;
  }
  return true;
}


function jstest(test){
  
  // --- Spit test from ],
  var att_obj = test.split("],");

  for (var i = 0; i < att_obj.length; i++){
  console.log(att_obj[i]);
  att_obj[i] = att_obj[i].replace(/[\[\](){}?*+\^$\\.|\-]/g, "\\$&");
  
  }

  console.log(att_obj);
}

function selectAll() 
{ 
    selectBox = document.getElementById("select1");

    for (var i = 0; i < selectBox.options.length; i++) 
    { 
         selectBox.options[i].selected = true; 
    } 

    selectBox = document.getElementById("select2");

    for (var i = 0; i < selectBox.options.length; i++) 
    { 
         selectBox.options[i].selected = true; 
    } 
}

function toggleDarkMode() {
  var element = document.body;
  element.classList.toggle("dark-mode");



  var sidebar = document.getElementById('sidebar');
  sidebar.classList.add('dark-mode');

}