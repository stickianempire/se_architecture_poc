async function fetchHtmlAsText(url) {
    return await (await fetch(url)).text();
}

async function loadWindow(name) {
    const contentDiv = document.getElementById("window");
    contentDiv.innerHTML = await fetchHtmlAsText("game/windows/"+name);
}