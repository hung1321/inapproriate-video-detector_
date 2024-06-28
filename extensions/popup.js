const btn = document.getElementById("summarise");
  var result;
btn.addEventListener("click", function() {
    btn.ariaDisabled = true;
    btn.innerHTML = "Đang kiểm tra.,, Vui lòng đợi!";
    chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
      let url = tabs[0].url;
      alert(url);
      var result;
        fetch('http://127.0.0.1:8000', 
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
              alert(data["result"][0]["label"]),
              console.log(data);
              if(data["result"][0]["label"]=="SFW"){
                document.getElementById("output").innerHTML = "video phù hợp với trẻ em"
                alert("Video phù hợp với trẻ em");
                btn.innerHTML = "Check";
              }
              else{
                document.getElementById("output").innerHTML = "video không phù hợp với trẻ em"
                alert("Video không phù hợp với trẻ em");
                btn.innerHTML="Check";

              }
            })
  });
});