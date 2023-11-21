<script>
	import { onMount } from 'svelte';
	import * as THREE from 'three';
	import * as SC from 'svelte-cubed';
	import {
		Header,
		HeaderNav,
		HeaderNavItem,
	} from "carbon-components-svelte"

	let name = "GoodAI";
	let socket;
	let frequency = 10;
	let size = 0.5;	// assign this an appropriate starting size
	let updatedFrequency = 10;
	let src = "images/logo-white.svg";

	// for spin of the 3D components
	let spin1 = 0;
	let spin2 = 0;
	let spin3 = 0;

	SC.onFrame(() => {
		spin1 += 0.01;
		spin2 += 0.02;
		spin3 += 0.005;
	});

	// Connect to websocket url and log connection message
	socket = new WebSocket('ws://0.0.0.0:8000/ws');

	// Execute upon connecting to websocket server:
	socket.onopen = () => {
		console.log('WebSocket connected');
		// Send initial frequency to backend
		socket.send(JSON.stringify({ frequency }));
    };

	// Define what happens when client recieved message from server
	socket.onmessage = (message) => {
		size = JSON.parse(message.data)['size'];
		console.log('Recieved data:', size); // log number recieved from server
	};


	// function to send frequency value to server
	const sendFrequency = () => {
		socket.send(JSON.stringify({ frequency }));
	};


	/**
	 * Update frequency value (also does not allow frequency value to be <1 and >30)
	 */
	function updateFrequencyAfterInput () {
		// get value in the text
		updatedFrequency = document.getElementById("frequencyText").value;

		// If input box is empty frequency remains as it was until it is updated with valid value
		if (updatedFrequency == '') {
			frequency = frequency;
		}
		// check if it is outside the desired range (1-30)
		else if (updatedFrequency > 30 || updatedFrequency < 1) {
			frequency = frequency;
			updatedFrequency = frequency;
			document.getElementById("frequencyText").value = frequency;
		}
		else {
			frequency = updatedFrequency;
		}
		sendFrequency();

	}



</script>



<!-- 3D components -->


<div class="grid-container">
	<SC.Canvas antialias background={new THREE.Color("rgb(34,34,36)")}>
		
		<!--Cube 3D component  -->
		<SC.Mesh 
			geometry={new THREE.BoxGeometry()} 
			material={new THREE.MeshStandardMaterial({ color: 0x03bafc })}
			scale={[size, size, size]}
			rotation={[spin1, spin1, spin1]}
			position={[-2.5,0,0]}
		/>

		<!-- Sphere 3D Component -->
		<SC.Mesh
			geometry={new THREE.SphereGeometry()}
			material={new THREE.MeshStandardMaterial({ color: 0xfa0724 })}
			rotation={[0, -spin2, 0]}
			scale={size}
		/>
		
		<!-- Cylinder 3D component -->
		<SC.Mesh 
			geometry={new THREE.CylinderGeometry()} 
			material={new THREE.MeshStandardMaterial({ color: 0xa670db })}
			scale={[size/2, size, size/2]}
			rotation={[spin3, spin3, spin3]}
			position={[2.5,0,0]}
		/>
		
		<SC.PerspectiveCamera position={[0, 0, 10]} />
		<SC.OrbitControls
			target={[0, 0, 0]}
			enableZoom={true}
			enablePan={true}
			enableDamping
			maxPolarAngle={Math.PI * 0.5}
		/>
		<SC.AmbientLight intensity={0.2} />
		<SC.DirectionalLight intensity={0.2} position={[-2, 3, 2]} />
	</SC.Canvas>
		
		
</div>  <!-- End of grid-container div -->



<!-- Header -->

<svelte:head>
  <link
    rel="stylesheet"
    href="https://unpkg.com/carbon-components-svelte/css/white.css"
  />
</svelte:head>

<Header company="GoodAI" platformName="Safe Artificial Intelligence">

</Header>

<slot />


<div class="block">
	<img src={src} alt="GoodAI" />
	<!-- <h1>Hello {name}!</h1> -->
	<div>
		<label for="frequency_label">Frequency:</label>
		<input id="frequencyText" type="number" bind:value={updatedFrequency} on:input={updateFrequencyAfterInput} min="1" max="30">
	</div>
</div>

<div class="instructions">
	<p>Left click and move mouse to rotate shapes.</p>
	<p>Hold left and right click to pan camera.</p>
	<p>Left click and move mouse to rotate shapes.</p>
</div>





<!-- Styling -->
<style>
	.block {
		position: absolute;
		top: 20%;
		left: 50%;
		transform: translate(-50%, -50%);
	}

	.instructions {
		color: aliceblue;
		position: fixed;
		left: 50%;
		bottom: 20px;
		transform: translate(-50%, -50%);
		margin: 0 auto;
	}

	div {
        margin-bottom: 10px;
		padding: 15px;
		margin: auto;
      }
      label {
		font-size: larger;
        display: inline-block;
        width: 110px;
        color: aliceblue;
      }

	input[type=number] {
		width: 5em;
		padding: 0.5em;
		border: .2em solid #7fbb42;
		border-radius: 1em;
		text-align: center;
		color: black;
		appearance: textfield;
		margin: 0;
		&::-webkit-inner-spin-button {
			opacity: 1;
			background: red;
		}
	}

	.grid-container {
		position: absolute;
		background: rgb(58, 63, 126);
		width: 100%;
		height: 100%;
		top: 0;
	}


</style>
