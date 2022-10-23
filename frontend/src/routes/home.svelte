<script>
  let message;

  fetch("http://127.0.0.1:1337/").then((response) => {
    response.json().then((json) => {
      message = json.msg;
    });
  });
</script>

<h1>{message}</h1>