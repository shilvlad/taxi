function window_open(href, width, height){
    window.open(href,'','Toolbar=0,Location=0,Directories=0,Status=0,Menubar=1,Scrollbars=0,Resizable=0 width=' + width + ',height=' + height + ',left=' + ((window.innerWidth - width)/2) + ',top=' + ((window.innerHeight - height)/2))
}