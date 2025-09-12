<script lang="ts">
  import TrophyCard from "./lib/Card.svelte";

  let trophies: {
    id: string;
    name: string;
    detail: string;
    hidden: boolean;
    ttype: string;
    pid: string;
  }[] = $state([]);

  let npCommId = $state("");

  const pullTrophies = async () => {
    const request = await fetch("http://localhost:5001/api/pull-trophies", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ np_comm_id: npCommId }),
    });

    if (request.status != 200) {
      console.error("Error while pulling trophies: ", request.status);
      return;
    }

    const response = await request.json();

    console.log(response);

    trophies = response["trophies"];
  };
</script>

<main class="w-full h-screen flex">
  <h1 class="text-2xl font-bold w-fit m-auto mt-5">PS4 Trophies</h1>
  <div class="flex w-full mt-10">
    <label
      for="search"
      class="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white"
      >Game COMM_ID</label
    >
    <div class="relative w-full">
      <div
        class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none"
      >
        <svg
          class="w-4 h-4 text-gray-500 dark:text-gray-400"
          aria-hidden="true"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 20 20"
        >
          <path
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"
          />
        </svg>
      </div>
      <input
        type="search"
        id="search"
        class="block w-full p-4 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 focus:outline-none"
        placeholder="Game COMM_ID"
        required
        bind:value={npCommId}
      />
      <button
        on:click={pullTrophies}
        class="cursor-pointer text-white absolute end-2.5 bottom-2.5 bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
        >Search</button
      >
    </div>
  </div>
  <div class="trophies-list flex flex-col gap-3 mt-5">
    <h2 class="text-lg">🏆 Trophies</h2>

    {#each trophies as trp, i}
      <TrophyCard
        id={trp.id}
        np_comm_id={npCommId}
        title={trp.name}
        description={trp.detail}
        ttype={trp.ttype}
      />
    {/each}
  </div>
</main>

<style>
  main {
    padding: 10px;
    max-width: 800px;
    height: 100vh;
    display: flex;
    flex-direction: column;
  }

  .trophies-list {
    flex: 1;
    overflow-y: auto;
    min-height: 0;
    padding-bottom: 0rem;
  }
</style>
