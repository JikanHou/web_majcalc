function avatar_upload(){
    const mask = document.getElementById('mask');
    if (mask == null)
        return;
    const avatar_input = document.getElementById('avatar-input');
    const avatar = document.getElementById('avatar');


    mask.onclick = function(){
        avatar_input.click();
    }
    avatar_input.onchange = function(){
        var input = avatar_input;
        var pic = input.files[0];
        if (input.value && pic.size <= 1024 * 1024 * 3){
            var formData = new FormData();
            formData.append('avatar', pic);
            $.ajax({
                url: '/avatar_upload',
                type: 'POST',
                cache: false,
                data: formData,
                processData: false,
                contentType: false
            }).fail(function(res){
                console.log(res);
                alert(res.responseText);
            }).success(function(res){
                var read = new FileReader();
                read.onload = function(e){
                    avatar.src = e.target.result;
                    document.getElementById('avatar_nav').src = e.target.result;
                }
                read.readAsDataURL(pic);
            })
        }
        else{
            if (input.value){
                alert('文件不能大于5MB');
            }
            return;
        }
    }
}

function window_onload(){
    avatar_upload();
    var btn = document.querySelector(".note-modify-btn");
    if (btn){ //本人登录
        btn.onclick = function(){

        }
    }
}

window.onload = window_onload;