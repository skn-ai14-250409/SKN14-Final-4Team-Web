const apiKey = "AIzaSyBs5WVEtocaAYuziY8TnDlnhwAUYbgqTdM"
const shortsBox = document.getElementById("shorts");


const Youtube = function(apiKey, $box) {
    const MAX_LOADS   = 50;
    const MAX_RESULTS = 10;

    async function getUploadPlaylistId(channelId) {
        const url = `https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id=${channelId}&key=${apiKey}`;
        const res = await fetch(url);
        const data = await res.json();
        return data.items[0].contentDetails.relatedPlaylists.uploads;
    }

    async function getVideosFromPlaylist(playlistId) {
        const url = `https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=${MAX_LOADS}&playlistId=${playlistId}&key=${apiKey}`;
        const res = await fetch(url);
        const data = await res.json();
        return data.items.map(item => item.contentDetails.videoId); // 랜덤 X

    }

    async function getShorts(videoIds) {
        const ids = videoIds.join(',');
        const url = `https://www.googleapis.com/youtube/v3/videos?part=contentDetails,snippet&id=${ids}&key=${apiKey}`;
        const res = await fetch(url);
        const data = await res.json();

        // 숏츠 먼저 필터링
        const shortsAll = data.items.filter(item => {
            const seconds = parseISODuration(item.contentDetails.duration);
            return seconds <= 60; // 숏츠 정의는 60초 이하
        });

        // 그 다음에 랜덤 섞기
        const shorts = shortsAll
            .sort(() => 0.5 - Math.random())
            .slice(0, 5)
            .map(item => ({
                title: item.snippet.title,
                embed: `https://www.youtube.com/embed/${item.id}`
            }));

        return shorts;
    }


    function parseISODuration(iso) {
        const regex = /PT(?:(\d+)M)?(?:(\d+)S)?/;
        const matches = iso.match(regex);
        return (parseInt(matches[1] || '0') * 60) + parseInt(matches[2] || '0');
    }

    // async function fetchShortsFromChannel(channelId) {
    //     try {
    //         const playlistId = await getUploadPlaylistId(channelId);
    //         const videoIds   = await getVideosFromPlaylist(playlistId);
    //         // const shorts     = await getVideoDetails(videoIds);
    //         const shorts_test = allVideos.filter(v => parseISODuration(v.contentDetails.duration) <= 60);
    //         const shorts = shorts_test.sort(() => 0.5 - Math.random()).slice(0, 5);


    //         $box.innerHTML = "";
    //         shorts.forEach(short => {
    //             const div = document.createElement("div");
    //             div.innerHTML = `
    //                 <iframe width="170" height="315" 
    //                     src="${short.embed}" 
    //                     title="${short.title}" 
    //                     allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
    //                     allowfullscreen>
    //                 </iframe>`;
    //             $box.appendChild(div);
    //         });
    //         $box.style.display = "flex";
    //     } catch (err) {
    //         console.error("Error fetching Shorts:", err);
    //     }
    // }

    async function fetchShortsFromChannel(channelId) {
        try {
            const playlistId = await getUploadPlaylistId(channelId);
            const videoIds = await getVideosFromPlaylist(playlistId);
            const shorts = await getShorts(videoIds);

            $box.innerHTML = "";
            shorts.forEach(short => {
                const div = document.createElement("div");
                div.innerHTML = `
                    <iframe width="170" height="300"
                        src="${short.embed}"
                        title="${short.title}"
                        allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                        allowfullscreen>
                    </iframe>`;
                $box.appendChild(div);
            });
            $box.style.display = "flex";
        } catch (err) {
            console.error("Error fetching Shorts:", err);
        }
    }

    return fetchShortsFromChannel;
};

// 초기화
const fetchShorts = Youtube(apiKey, shortsBox);

// 로딩 표시
function showLoading(ai_id) {
    document.querySelector(".typing-indicator").style.display = "flex";
    const channelId = AIShortsChannels[ai_id]; // html or js에서 매핑 필요
    if (channelId) {
        fetchShorts(channelId);
    }
}
function hideLoading() {
    document.querySelector(".typing-indicator").style.display = "none";
    shortsBox.style.display = "none";
}
