const btn = document.getElementById("summarise");
  var result;
btn.addEventListener("click", function() {
    btn.disabled = true;
    btn.innerHTML = "Đang kiểm tra... Vui lòng đợi!";
    chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
      let url = tabs[0].url;
      //alert(url);
      var result;
        fetch('https://tinhoctre-server4-pajveyvcjq-et.a.run.app', 
            {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              'url': url
            })
          }).then(response => response.json())
            .then(data => {
              //alert(data["result"][0]["label"]),
              if(data["check"]!="Fail"){
              console.log(data);
              if(data["result"]=="SFW"){
                document.getElementById("output").innerHTML = "video phù hợp với trẻ em!!!!!";
                alert("Video phù hợp với trẻ em");
                
                btn.innerHTML = "Kiểm tra";
                btn.disabled = false;
              }
              else{
                document.getElementById("output").innerHTML = "Video được khuyến cáo không phù hợp với trẻ em!";
                document.getElementById("quanity").innerHTML = "Số lượng câu không phù hợp: "+data["count_toxic"];
                alert("Video không phù hợp với trẻ em!!!!!");
                btn.innerHTML="Kiểm Tra";
                btn.disabled = false;
              }
            }
            else{
              document.getElementById("output").innerHTML = "Hệ thống chưa hỗ trợ định dạng video này vui lòng thử với video có phụ đề tiếng Anh";
              btn.innerHTML = "Kiểm tra";
              btn.disabled = false
            }
            })
  });
});