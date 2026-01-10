'use strict';
const MANIFEST = 'flutter-app-manifest';
const TEMP = 'flutter-temp-cache';
const CACHE_NAME = 'flutter-app-cache';

const RESOURCES = {"assets/AssetManifest.bin": "8cd033f2f627d98a3613eae12f963f5d",
"assets/AssetManifest.bin.json": "a29671d66f45a2cdc4dfaff6a42ff0c2",
"assets/assets/icons/add.png": "872d11d0741d7f5ae46bf20223095394",
"assets/assets/icons/Approved_Red.png": "325a2b5b6c27b0baa1856e65bbcdf860",
"assets/assets/icons/audit.png": "acf0b5518cd31a6a958d7d272b7e0ae8",
"assets/assets/icons/audits.png": "2333ab54a0111ac702c8a248b194d798",
"assets/assets/icons/Calendar_Date%2520Picker_Red.png": "d70b42616e6b122006942c9fc17642c1",
"assets/assets/icons/calendar_icon.png": "5d1e6eb240070919089756a6bcdf2d1f",
"assets/assets/icons/candidates.png": "472fdb70d59082319b51e5f0baa000b8",
"assets/assets/icons/Chatbot_Red.png": "c9ac98884d2ba457159993bd4427cc2a",
"assets/assets/icons/data-analytics.png": "05fb4be5ff64f63ef9403707d8f0ce9c",
"assets/assets/icons/facebook.png": "e4da23704f27c9df07e6c21a13e28bfd",
"assets/assets/icons/facebook1.png": "14150615fbf19b940f52520488fe40fb",
"assets/assets/icons/google.png": "b92d750297623c2ccb2c646777f9b3c3",
"assets/assets/icons/Growth_Development_Red%2520Badge_White.png": "db5797076a065209e7abe46dad7146b4",
"assets/assets/icons/Information_Red%2520Badge_White.png": "2d7346951213fd9c8a495dab7427e811",
"assets/assets/icons/Instagram.png": "9e592ff7876ffc7dfbeb483f1860983c",
"assets/assets/icons/Instagram1.png": "6fd95a7d52356ffb4a9458008b5632c6",
"assets/assets/icons/interview.png": "496a4ad71785622d71c98192e79b9ae9",
"assets/assets/icons/jobs.png": "40ea56df4c8f8468f365b8346ab2405b",
"assets/assets/icons/khono.png": "a71298a29c3d7794173d28e6e1a8825c",
"assets/assets/icons/LinkedIn.png": "4318ee497dc101c3f47a88c1d996eb11",
"assets/assets/icons/LinkedIn1.png": "53aad070ec3c02726a011ba0db9a5f2c",
"assets/assets/icons/Lock_Red%2520Badge_White.png": "9aabbcd716a834678453e90e45c930c3",
"assets/assets/icons/Logout_Red%2520Badge_White.png": "f3b64cabc6492a3c229eb9a1baf6b5a1",
"assets/assets/icons/microsoft.png": "49c2774948c09b4902cd23299709c48f",
"assets/assets/icons/notification.png": "71d1e7e8d4eaf5c8ccdadd69cbeaeae9",
"assets/assets/icons/okta.png": "0e3ba9d8c2e329e487a9bae004606f0d",
"assets/assets/icons/pbi.png": "f10d987316943495ecbe2b28899340e8",
"assets/assets/icons/Project%2520Launch_Start_Red%2520Badge_White.png": "7b9eea159b0a829ce30d9438cc3fc487",
"assets/assets/icons/Red_chnage%2520password_badge.png": "89e713fa9f12b93ab6868af002fe60d3",
"assets/assets/icons/RED_Settings%2520icon%2520badge.png": "affe2a4adbbcaccdafb3bf3eb9bcb8a6",
"assets/assets/icons/red_user_profile.png": "5e20a1e0822113ab5342039d1dbd2e5c",
"assets/assets/icons/review.png": "7eb9a2e25797e51ebf9afffa19babcea",
"assets/assets/icons/saml.png": "2f5d264be4a8e46411f50b2896ac6193",
"assets/assets/icons/teamC.png": "d35bddb79a2468570c0a7f53c925fcfa",
"assets/assets/icons/team_icon.png": "8f6c88f798b2a7cc9d189e7e890c0837",
"assets/assets/icons/Upload%2520Arrow_Red%2520Badge_White.png": "db64c921b6c23f5d18c9aab8f7d4b4f4",
"assets/assets/icons/Upload%2520Arrow_Red.png": "d4b30373b58f4d0a351672ab9a417c8a",
"assets/assets/icons/User_Profile_White_Badge_Red.png": "ed4341787e975065578b320564350de1",
"assets/assets/icons/x1.png": "7105f60bc49b3855b6b18b4e167ec7a8",
"assets/assets/icons/YouTube.png": "704138bd1c85128058f1e24bf0f39aa8",
"assets/assets/icons/YouTube1.png": "6a44a2c7deca37d38a985d8ebb5d64d7",
"assets/assets/images/bg.jpg": "a641af61397045cff6d88e6f19b83bd3",
"assets/assets/images/bg1.jpg": "b239ecb8a14e75c35445d08395989890",
"assets/assets/images/bg2.jpg": "72c5228cdba80d4298d06403bb5c5306",
"assets/assets/images/bg3.jpeg": "db7485fcf2fc76d479ac3644c21a109e",
"assets/assets/images/bg4.jpg": "83e5c585fd677bea5ce834efd7bbb324",
"assets/assets/images/chatbot.png": "244d2fcf1e5f2b7eeb99aa7ce323db92",
"assets/assets/images/client0.png": "ef17e6259c69d1ae233586d647d2f529",
"assets/assets/images/client1.png": "431ba669c3601730eebeaf637615c099",
"assets/assets/images/client2.png": "78b9128a9eeb97b21302ededa6654ad2",
"assets/assets/images/client3.png": "fbb0830653b2e2c935cf501402aa5593",
"assets/assets/images/client4.png": "02c6f2ae44826aea21fdb8f9a1d08d2a",
"assets/assets/images/client5.png": "681365bb840d54df7bf67fbbb50f877a",
"assets/assets/images/collaggge.jpg": "cfa42ba67bca731661e53f8883b572a4",
"assets/assets/images/dark.png": "f430380cb1fd87043135b6bb5824ab05",
"assets/assets/images/default.jpeg": "6cdefaa64fd7ab4b91e47428824ee112",
"assets/assets/images/final.jpg": "2d5098a2500010192b779d4708c059e0",
"assets/assets/images/icon.png": "d1cbe7584d6f4ffb73c84ae486288003",
"assets/assets/images/logo.png": "fab0fd539e1d6b2e7a8d9168e5ececcd",
"assets/assets/images/logo2.png": "a71298a29c3d7794173d28e6e1a8825c",
"assets/assets/images/logo3.png": "3e4271fcb09b0d70aeb59ee3183bf11a",
"assets/assets/images/logow.png": "5b5c0913ea344bc478cebfc709805ceb",
"assets/assets/images/Mosa.jpg": "14796ffb949b7982b015233bae2372b9",
"assets/assets/images/Nathi_design_3.png": "f430380cb1fd87043135b6bb5824ab05",
"assets/assets/images/office.jpg": "04553418db5784d8ffd148ee3a1dcc77",
"assets/assets/images/profile_placeholder.png": "52cb531e6df578a9ffa7991f6f288907",
"assets/assets/images/SearchRed.png": "d50cf682e707f3618f3bce95e3de15d3",
"assets/assets/images/simba.jpg": "8c73353b43bb82d0d418013d3e6238b8",
"assets/assets/images/team0.jpg": "cfa42ba67bca731661e53f8883b572a4",
"assets/assets/images/team1.jpg": "3c95a0b43c8c81c97afe27b5fbc93ead",
"assets/assets/images/team2.jpg": "14796ffb949b7982b015233bae2372b9",
"assets/assets/images/team3.jpg": "c18badd152745f30a5d56708072a7c57",
"assets/assets/images/team4.jpg": "79444583d0cde860630fcf1753ddbfc3",
"assets/assets/images/team5.jpg": "04553418db5784d8ffd148ee3a1dcc77",
"assets/assets/images/thato.png": "2306bddbabf41a8dff926500776601e0",
"assets/assets/images/wallpaper.jpeg": "8790faf8248f7f23b818e601021c859f",
"assets/FontManifest.json": "3ddd9b2ab1c2ae162d46e3cc7b78ba88",
"assets/fonts/MaterialIcons-Regular.otf": "98b8131e8327d070372ff39a7ec29067",
"assets/NOTICES": "5c5c5d39a467af3431210c4338132902",
"assets/packages/font_awesome_flutter/lib/fonts/fa-brands-400.ttf": "ce3c7b3522600b745b93ed0d62347080",
"assets/packages/font_awesome_flutter/lib/fonts/fa-regular-400.ttf": "262525e2081311609d1fdab966c82bfc",
"assets/packages/font_awesome_flutter/lib/fonts/fa-solid-900.ttf": "269f971cec0d5dc864fe9ae080b19e23",
"assets/packages/timezone/data/latest_all.tzf": "5e6af46f7fdd153c308fc6531ba69d03",
"assets/shaders/ink_sparkle.frag": "ecc85a2e95f5e9f53123dcaf8cb9b6ce",
"assets/shaders/stretch_effect.frag": "40d68efbbf360632f614c731219e95f0",
"auth-callback.html": "2fb35f07e7f192c3203236f42fcbbd8e",
"canvaskit/canvaskit.js": "8331fe38e66b3a898c4f37648aaf7ee2",
"canvaskit/canvaskit.js.symbols": "a3c9f77715b642d0437d9c275caba91e",
"canvaskit/canvaskit.wasm": "9b6a7830bf26959b200594729d73538e",
"canvaskit/chromium/canvaskit.js": "a80c765aaa8af8645c9fb1aae53f9abf",
"canvaskit/chromium/canvaskit.js.symbols": "e2d09f0e434bc118bf67dae526737d07",
"canvaskit/chromium/canvaskit.wasm": "a726e3f75a84fcdf495a15817c63a35d",
"canvaskit/skwasm.js": "8060d46e9a4901ca9991edd3a26be4f0",
"canvaskit/skwasm.js.symbols": "3a4aadf4e8141f284bd524976b1d6bdc",
"canvaskit/skwasm.wasm": "7e5f3afdd3b0747a1fd4517cea239898",
"canvaskit/skwasm_heavy.js": "740d43a6b8240ef9e23eed8c48840da4",
"canvaskit/skwasm_heavy.js.symbols": "0755b4fb399918388d71b59ad390b055",
"canvaskit/skwasm_heavy.wasm": "b0be7910760d205ea4e011458df6ee01",
"favicon.png": "5dcef449791fa27946b3d35ad8803796",
"flutter.js": "24bc71911b75b5f8135c949e27a2984e",
"flutter_bootstrap.js": "b1f19f009026ab0f41cd0a79e2493750",
"icons/Icon-192.png": "ac9a721a12bbc803b44f645561ecb1e1",
"icons/Icon-512.png": "96e752610906ba2a93c65f8abe1645f1",
"icons/Icon-maskable-192.png": "c457ef57daa1d16f64b27b786ec2ea3c",
"icons/Icon-maskable-512.png": "301a7604d45b3e739efc881eb04896ea",
"index.html": "04586611f0215a0f52a9dff76722e896",
"/": "04586611f0215a0f52a9dff76722e896",
"main.dart.js": "98a7020b8c9fabb5145cdcf61cc904bd",
"manifest.json": "85a94bf261ef3f48d1085195886e084a",
"version.json": "e7c46e16d5024ef7867c35c61746d35b"};
// The application shell files that are downloaded before a service worker can
// start.
const CORE = ["main.dart.js",
"index.html",
"flutter_bootstrap.js",
"assets/AssetManifest.bin.json",
"assets/FontManifest.json"];

// During install, the TEMP cache is populated with the application shell files.
self.addEventListener("install", (event) => {
  self.skipWaiting();
  return event.waitUntil(
    caches.open(TEMP).then((cache) => {
      return cache.addAll(
        CORE.map((value) => new Request(value, {'cache': 'reload'})));
    })
  );
});
// During activate, the cache is populated with the temp files downloaded in
// install. If this service worker is upgrading from one with a saved
// MANIFEST, then use this to retain unchanged resource files.
self.addEventListener("activate", function(event) {
  return event.waitUntil(async function() {
    try {
      var contentCache = await caches.open(CACHE_NAME);
      var tempCache = await caches.open(TEMP);
      var manifestCache = await caches.open(MANIFEST);
      var manifest = await manifestCache.match('manifest');
      // When there is no prior manifest, clear the entire cache.
      if (!manifest) {
        await caches.delete(CACHE_NAME);
        contentCache = await caches.open(CACHE_NAME);
        for (var request of await tempCache.keys()) {
          var response = await tempCache.match(request);
          await contentCache.put(request, response);
        }
        await caches.delete(TEMP);
        // Save the manifest to make future upgrades efficient.
        await manifestCache.put('manifest', new Response(JSON.stringify(RESOURCES)));
        // Claim client to enable caching on first launch
        self.clients.claim();
        return;
      }
      var oldManifest = await manifest.json();
      var origin = self.location.origin;
      for (var request of await contentCache.keys()) {
        var key = request.url.substring(origin.length + 1);
        if (key == "") {
          key = "/";
        }
        // If a resource from the old manifest is not in the new cache, or if
        // the MD5 sum has changed, delete it. Otherwise the resource is left
        // in the cache and can be reused by the new service worker.
        if (!RESOURCES[key] || RESOURCES[key] != oldManifest[key]) {
          await contentCache.delete(request);
        }
      }
      // Populate the cache with the app shell TEMP files, potentially overwriting
      // cache files preserved above.
      for (var request of await tempCache.keys()) {
        var response = await tempCache.match(request);
        await contentCache.put(request, response);
      }
      await caches.delete(TEMP);
      // Save the manifest to make future upgrades efficient.
      await manifestCache.put('manifest', new Response(JSON.stringify(RESOURCES)));
      // Claim client to enable caching on first launch
      self.clients.claim();
      return;
    } catch (err) {
      // On an unhandled exception the state of the cache cannot be guaranteed.
      console.error('Failed to upgrade service worker: ' + err);
      await caches.delete(CACHE_NAME);
      await caches.delete(TEMP);
      await caches.delete(MANIFEST);
    }
  }());
});
// The fetch handler redirects requests for RESOURCE files to the service
// worker cache.
self.addEventListener("fetch", (event) => {
  if (event.request.method !== 'GET') {
    return;
  }
  var origin = self.location.origin;
  var key = event.request.url.substring(origin.length + 1);
  // Redirect URLs to the index.html
  if (key.indexOf('?v=') != -1) {
    key = key.split('?v=')[0];
  }
  if (event.request.url == origin || event.request.url.startsWith(origin + '/#') || key == '') {
    key = '/';
  }
  // If the URL is not the RESOURCE list then return to signal that the
  // browser should take over.
  if (!RESOURCES[key]) {
    return;
  }
  // If the URL is the index.html, perform an online-first request.
  if (key == '/') {
    return onlineFirst(event);
  }
  event.respondWith(caches.open(CACHE_NAME)
    .then((cache) =>  {
      return cache.match(event.request).then((response) => {
        // Either respond with the cached resource, or perform a fetch and
        // lazily populate the cache only if the resource was successfully fetched.
        return response || fetch(event.request).then((response) => {
          if (response && Boolean(response.ok)) {
            cache.put(event.request, response.clone());
          }
          return response;
        });
      })
    })
  );
});
self.addEventListener('message', (event) => {
  // SkipWaiting can be used to immediately activate a waiting service worker.
  // This will also require a page refresh triggered by the main worker.
  if (event.data === 'skipWaiting') {
    self.skipWaiting();
    return;
  }
  if (event.data === 'downloadOffline') {
    downloadOffline();
    return;
  }
});
// Download offline will check the RESOURCES for all files not in the cache
// and populate them.
async function downloadOffline() {
  var resources = [];
  var contentCache = await caches.open(CACHE_NAME);
  var currentContent = {};
  for (var request of await contentCache.keys()) {
    var key = request.url.substring(origin.length + 1);
    if (key == "") {
      key = "/";
    }
    currentContent[key] = true;
  }
  for (var resourceKey of Object.keys(RESOURCES)) {
    if (!currentContent[resourceKey]) {
      resources.push(resourceKey);
    }
  }
  return contentCache.addAll(resources);
}
// Attempt to download the resource online before falling back to
// the offline cache.
function onlineFirst(event) {
  return event.respondWith(
    fetch(event.request).then((response) => {
      return caches.open(CACHE_NAME).then((cache) => {
        cache.put(event.request, response.clone());
        return response;
      });
    }).catch((error) => {
      return caches.open(CACHE_NAME).then((cache) => {
        return cache.match(event.request).then((response) => {
          if (response != null) {
            return response;
          }
          throw error;
        });
      });
    })
  );
}
