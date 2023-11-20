<script>
	import { onMount } from 'svelte';
	import * as THREE from 'three';
	import * as SC from 'svelte-cubed';

	let name = "GoodAI";
	let socket;
	let frequency = 10;
	let size = 0.5;	// assign this an appropriate starting size
	let updatedFrequency = 10;

	// for spin of the 3D components
	let spin1 = 0;
	let spin2 = 0;
	let spin3 = 0;

	SC.onFrame(() => {
		spin1 += 0.01;
		spin2 += 0.02;
		spin3 += 0.005;
	});

	// On spawn?
	onMount(() => {

		
	}); // End of onMount

	// Connect to websocket url and log connection message
	socket = new WebSocket('ws://0.0.0.0:8080/ws');

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


	// function to update frequency value (also does not allow frequency value to be <1 and >30)
	function updateFrequencyAfterInput () {
		// get value in the text
		updatedFrequency = document.getElementById("frequencyText").value;

		// check if it is outside the desired range (1-30)
		if (updatedFrequency > 30 || updatedFrequency < 1) {
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
<div class="container">
	<SC.Canvas antialias background={new THREE.Color('papayawhip')}>
		
		<!--Cube 3D component  -->
		<SC.Mesh 
			geometry={new THREE.BoxGeometry()} 
			material={new THREE.MeshStandardMaterial({ color: 0xff3e00 })}
			scale={[size, size, size]}
			rotation={[spin1, spin1, spin1]}
			castshadow
			position={[-2.5,0,0]}
		/>

		<!-- Sphere 3D Component -->
		<SC.Mesh
			geometry={new THREE.SphereGeometry()}
			material={new THREE.MeshStandardMaterial({ color: 0xffff00 })}
			rotation={[0, -spin2, 0]}
			scale={size}
		/>
		
		<!-- Cylinder 3D component -->
		<SC.Mesh 
			geometry={new THREE.CylinderGeometry()} 
			material={new THREE.MeshStandardMaterial({ color: 0xff3e00 })}
			scale={[size/2, size, size/2]}
			rotation={[spin3, spin3, spin3]}
			castshadow
			position={[2.5,0,0]}
		/>
		
		<SC.PerspectiveCamera position={[0, 0, 10]} />
		<SC.OrbitControls
			target={[0, 0, 0]}
			enableZoom={false}
			enablePan={false}
			enableDamping
			maxPolarAngle={Math.PI * 0.5}
		/>
		<SC.AmbientLight intensity={0.2} />
		<SC.DirectionalLight intensity={0.2} position={[-2, 3, 2]} />
	</SC.Canvas>
		
</div>


<div class="block">
	<h1>Hello {name}!</h1>
	<div>
		<label for="frequency_label">Frequency:</label>
		<input id="frequencyText" type="number" bind:value={updatedFrequency} on:input={updateFrequencyAfterInput} min="1" max="30">
	</div>
	
</div>



<!-- Styling -->
<style>
	div {
        margin-bottom: 10px;
      }
      label {
		font-size: larger;
        display: inline-block;
        width: 110px;
        color: #777777;
      }
      input {
        padding: 5px 10px;
		width: 60px;
		border: 1px solid #000000;
      }

	.container {
		position: absolute;
		background: rgb(58, 63, 126);
		width: 100%;
		height: 100%;
		top: 0;
	}


	.block {
		position: absolute;
		top: 20%;
		left: 50%;
		transform: translate(-50%, -50%);
	}

</style>
