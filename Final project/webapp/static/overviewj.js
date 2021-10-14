console.log("1342323");
form=document.getElementById('form_value').innerHTML;
    if (form==0){
        document.getElementById('under').setAttribute("class", "text-white");
    }   else if (form>0){
        document.getElementById('prerace').setAttribute("class","text-white");
    }   else if (form<-20){
        document.getElementById('over').setAttribute("class","text-white");
    }   else {
        document.getElementById('optimal').setAttribute("class","text-white");
    }