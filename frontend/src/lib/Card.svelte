<script lang="ts">
    let props: {
        id: string;
        np_comm_id: string;
        title: string;
        description: string;
        ttype: string;
    } = $props();
</script>

<a
    href="#"
    class="flex flex-col h-20 items-center bg-white border border-gray-200 rounded-lg shadow-sm flex-row hover:bg-gray-100 dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-700"
>
    <img
        class="object-cover h-full rounded-l-md"
        src={`http://localhost:5001/static/${props.np_comm_id}/TROP${props.id}.PNG`}
        alt=""
    />
    <div class="flex w-full items-center justify-between p-4 leading-normal">
        <div class="flex flex-col">
            <span
                class="text-xl font-bold tracking-tight text-gray-900 dark:text-white"
            >
                {props.title}
            </span>
            <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">
                {props.description}
            </p>
        </div>
        <div>
            {#if props.ttype === "PLATINUM"}
                <span
                    class="inline-flex items-center justify-center w-10 h-10 me-2 text-sm font-semibold text-gray-800 bg-[#163c90] rounded-full dark:text-gray-300"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="32"
                        height="32"
                        viewBox="0 0 24 24"
                        ><!-- Icon from Material Symbols by Google - https://github.com/google/material-design-icons/blob/master/LICENSE --><path
                            fill="currentColor"
                            d="M7 21v-2h4v-3.1q-1.225-.275-2.187-1.037T7.4 12.95q-1.875-.225-3.137-1.637T3 8V7q0-.825.588-1.412T5 5h2V3h10v2h2q.825 0 1.413.588T21 7v1q0 1.9-1.263 3.313T16.6 12.95q-.45 1.15-1.412 1.913T13 15.9V19h4v2zm0-10.2V7H5v1q0 .95.55 1.713T7 10.8m10 0q.9-.325 1.45-1.088T19 8V7h-2z"
                        /></svg
                    ></span
                >
            {:else if props.ttype === "GOLD"}
                <span
                    class="inline-flex items-center justify-center w-10 h-10 me-2 text-sm font-semibold text-gray-800 bg-[#FFD700] rounded-full dark:text-gray-300"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="32"
                        height="32"
                        viewBox="0 0 24 24"
                        ><!-- Icon from Material Symbols by Google - https://github.com/google/material-design-icons/blob/master/LICENSE --><path
                            fill="grey"
                            d="M7 21v-2h4v-3.1q-1.225-.275-2.187-1.037T7.4 12.95q-1.875-.225-3.137-1.637T3 8V7q0-.825.588-1.412T5 5h2V3h10v2h2q.825 0 1.413.588T21 7v1q0 1.9-1.263 3.313T16.6 12.95q-.45 1.15-1.412 1.913T13 15.9V19h4v2zm0-10.2V7H5v1q0 .95.55 1.713T7 10.8m10 0q.9-.325 1.45-1.088T19 8V7h-2z"
                        /></svg
                    ></span
                >{:else if props.ttype === "SILVER"}
                <span
                    class="inline-flex items-center justify-center w-10 h-10 me-2 text-sm font-semibold text-gray-800 bg-gray-500 rounded-full dark:text-gray-300"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="32"
                        height="32"
                        viewBox="0 0 24 24"
                        ><!-- Icon from Material Symbols by Google - https://github.com/google/material-design-icons/blob/master/LICENSE --><path
                            fill="currentColor"
                            d="M7 21v-2h4v-3.1q-1.225-.275-2.187-1.037T7.4 12.95q-1.875-.225-3.137-1.637T3 8V7q0-.825.588-1.412T5 5h2V3h10v2h2q.825 0 1.413.588T21 7v1q0 1.9-1.263 3.313T16.6 12.95q-.45 1.15-1.412 1.913T13 15.9V19h4v2zm0-10.2V7H5v1q0 .95.55 1.713T7 10.8m10 0q.9-.325 1.45-1.088T19 8V7h-2z"
                        /></svg
                    ></span
                >{:else if props.ttype === "BRONZE"}
                <span
                    class="inline-flex items-center justify-center w-10 h-10 me-2 text-sm font-semibold text-gray-800 bg-stone-800 rounded-full dark:text-gray-300"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="32"
                        height="32"
                        viewBox="0 0 24 24"
                        ><!-- Icon from Material Symbols by Google - https://github.com/google/material-design-icons/blob/master/LICENSE --><path
                            fill="currentColor"
                            d="M7 21v-2h4v-3.1q-1.225-.275-2.187-1.037T7.4 12.95q-1.875-.225-3.137-1.637T3 8V7q0-.825.588-1.412T5 5h2V3h10v2h2q.825 0 1.413.588T21 7v1q0 1.9-1.263 3.313T16.6 12.95q-.45 1.15-1.412 1.913T13 15.9V19h4v2zm0-10.2V7H5v1q0 .95.55 1.713T7 10.8m10 0q.9-.325 1.45-1.088T19 8V7h-2z"
                        /></svg
                    ></span
                >{/if}
        </div>
    </div>
</a>
