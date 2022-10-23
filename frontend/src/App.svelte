<!-- <script>
  let message;

  fetch("http://127.0.0.1:1337/").then((response) => {
    response.json().then((json) => {
      message = json.msg;
    });
  });
  import {Router, Link, Route} from "svelte-spa-router"
</script>

<h1>{message}</h1> -->

<script>
  import Router from 'svelte-spa-router'
  import Home from "./routes/home.svelte"

  const routes = {
    '/': Home,
  }
</script>

<Router {routes}/>