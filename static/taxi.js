function window_open_(href, width, height){
    window.open(href,'','Toolbar=0,Location=0,Directories=0,Status=0,Menubar=1,Scrollbars=0,Resizable=0 width=' + width + ',height=' + height + ',left=' + ((window.innerWidth - width)/2) + ',top=' + ((window.innerHeight - height)/2))
}

function window_open(href, width, height, state){
    document.getElementById('window').style.display = state;
    document.getElementById('wrap').style.display = state;
}

function show(state, href){

					document.getElementById('window').style.display = state;
					document.getElementById('wrap').style.display = state;
					$('.content').load(href);
                    //$('.content').append('<p>***</p>');
			}
