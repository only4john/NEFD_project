// --- This is the final, corrected map.js using the correct view name ---

const map = new maplibregl.Map({
    container: 'map',
    // --- 将下面这一行替换掉 ---
    // style: 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json', 

    // --- 换成这一行 ---
    style: 'https://tiles.stadiamaps.com/styles/alidade_smooth.json', // 使用 Stadia Maps 作为备用底图

    center: [173, -41.5],
    zoom: 4.5
});

map.addControl(new maplibregl.NavigationControl(), 'top-right');

map.on('load', () => {
    console.log('[DEBUG] Map loaded. Adding MASTER VIEW data source...');

    // --- CRITICAL FIX #1 ---
    // We are now requesting the correct view: "master_forestry_view"
    map.addSource('master-source', {
        type: 'vector',
        tiles: [`http://localhost:7800/public.master_forestry_view/{z}/{x}/{y}.pbf?cachebust=${Date.now()}`]
    });
    console.log('[DEBUG] MASTER VIEW source "master-source" added.');

    map.addLayer({
        'id': 'master-fill-layer',
        'type': 'fill',
        'source': 'master-source',
        // --- CRITICAL FIX #2 ---
        // The source-layer must also match the correct view name
        'source-layer': 'public.master_forestry_view',
        'paint': {
            'fill-color': '#FF00FF', // Let's keep it bright pink for the final test
            'fill-opacity': 0.7
        }
    }, 'waterway');
    console.log('[DEBUG] MASTER VIEW layer "master-fill-layer" added.');
});

map.on('error', (e) => {
    console.error("❌ A map error occurred:", e);
});