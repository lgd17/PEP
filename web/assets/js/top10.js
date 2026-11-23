let allMatches = [];

function formatDate(dateString) {

    if (!dateString) {
        return "-";
    }

    const date = new Date(dateString);

    return date.toLocaleString(
        "fr-FR",
        {
            dateStyle: "medium",
            timeStyle: "short"
        }
    );
}

function createCard(match) {

    const homeLogo =
        match.home_logo || "";

    const awayLogo =
        match.away_logo || "";

    const flagEmoji =
        match.country?.emoji || "🏆";

    return `

    <div class="card">

        <div class="header">

            <div class="rank">
                🏆 #${match.rank}
            </div>

            <div class="badge">
                ACTIF ✅
            </div>

        </div>

        <div class="competition">

            ${flagEmoji}
            ${match.competition}

        </div>

        <div class="match-time">

            🗓 ${formatDate(match.event_date)}

        </div>

        <div class="teams">

            <img
                class="logo"
                src="${homeLogo}"
                alt="${match.home_team}"
            >

            <div class="vs">
                VS
            </div>

            <img
                class="logo"
                src="${awayLogo}"
                alt="${match.away_team}"
            >

        </div>

        <div class="match-name">

            ${match.home_team}
            vs
            ${match.away_team}

        </div>

        <div class="score-box">

            📊 Score XPRONOS

            <div class="xpronos">

                ${match.score_xpronos}

            </div>

        </div>

        <div class="pick pick-primary">

            ✅ ${match.best_pick.market}

            (${match.best_pick.confidence}%)

        </div>

        <div class="pick pick-secondary">

            ✅ ${match.second_pick.market}

            (${match.second_pick.confidence}%)

        </div>

        <div class="exact-score">

            🎯 Score exact :

            ${match.best_exact_score.score}

        </div>

    </div>

    `;
}

function renderMatches(league = "all") {

    const container =
        document.getElementById(
            "matchesContainer"
        );

    if (!container) {
        return;
    }

    container.innerHTML = "";

    let matches = allMatches;

    if (league !== "all") {

        matches = matches.filter(
            match =>
                match.competition === league
        );
    }

    matches.forEach(match => {

        container.innerHTML +=
            createCard(match);

    });
}

function initLeagueFilter() {

    const filter =
        document.getElementById(
            "leagueFilter"
        );

    if (!filter) {
        return;
    }

    const leagues = [

        ...new Set(

            allMatches.map(
                match =>
                    match.competition
            )

        )

    ];

    leagues.forEach(league => {

        const option =
            document.createElement(
                "option"
            );

        option.value = league;

        option.textContent = league;

ole.error(error);

        document
            .getElementById(
                "matchesContainer"
            )
            .innerHTML =
            `
            <div class="card">
                Impossible de charger le Top 10.
            </div>
            `;
    }
}

document.addEventListener(
    "DOMContentLoaded",
    loadTop10
);
                  
let allMatches = [];

function formatDate(dateString) {

    if (!dateString) {
        return "-";
    }

    const date = new Date(dateString);

    return date.toLocaleString(
        "fr-FR",
        {
            dateStyle: "medium",
            timeStyle: "short"
        }
    );
}

function createCard(match) {

    const homeLogo =
        match.home_logo || "";

    const awayLogo =
        match.away_logo || "";

    const rank =
        match.rank || "-";

    const competition =
        match.competition || "Compétition";

    const flagEmoji =
        match.country?.emoji || "🏆";

    const scoreXpronos =
        Number(
            match.score_xpronos || 0
        ).toFixed(1);

    const bestPick =
        match.best_pick || {};

    const secondPick =
        match.second_pick || {};

    const exactScore =
        match.best_exact_score || {};

    return `

    <div class="card">

        <div class="card-header">

            <div class="rank">
                🏆 #${rank}
            </div>

            <div class="status">
                ACTIF ✅
            </div>

        </div>

        <div class="competition">

            ${flagEmoji}
            ${competition}

        </div>

        <div class="match-time">

            🗓 ${formatDate(
                match.event_date
            )}

        </div>

        <div class="teams">

            <img
                class="logo"
                src="${homeLogo}"
                alt="${match.home_team || ''}"
                loading="lazy"
            >

            <div class="vs">
                VS
            </div>

            <img
                class="logo"
                src="${awayLogo}"
                alt="${match.away_team || ''}"
                loading="lazy"
            >

        </div>

        <div class="match-name">

            ${match.home_team || '-'}

            vs

            ${match.away_team || '-'}

        </div>

        <div class="score-box">

            <div class="score-label">

                📊 Score XPRONOS

            </div>

            <div class="score-value">

                ${scoreXpronos}

            </div>

        </div>

        <div class="pick primary">

            ✅ ${bestPick.market || "-"}

            (${bestPick.confidence || 0}%)

            ${bestPick.odds
                ? `• 💰 ${bestPick.odds}`
                : ""
            }

        </div>

        <div class="pick secondary">

            ✅ ${secondPick.market || "-"}

            (${secondPick.confidence || 0}%)

            ${secondPick.odds
                ? `• 💰 ${secondPick.odds}`
                : ""
            }

        </div>

        <div class="exact">

            🎯 Score exact :

            ${exactScore.score || "-"}

        </div>

    </div>

    `;
}

function renderMatches(
    league = "all"
) {

    const container =
        document.getElementById(
            "matchesContainer"
        );

    if (!container) {
        return;
    }

    container.innerHTML = "";

    let matches =
        [...allMatches];

    if (
        league !== "all"
    ) {

        matches =
            matches.filter(
                match =>
                    match.competition === league
            );
    }

    matches.forEach(
        match => {

            container.innerHTML +=
                createCard(match);

        }
    );

    if (
        matches.length === 0
    ) {
let allMatches = [];

function formatDate(dateString) {

    if (!dateString) {
        return "-";
    }

    const date = new Date(dateString);

    return date.toLocaleString(
        "fr-FR",
        {
            dateStyle: "medium",
            timeStyle: "short"
        }
    );
}

function createCard(match) {

    const homeLogo =
        match.home_logo || "";

    const awayLogo =
        match.away_logo || "";

    const rank =
        match.rank || "-";

    const competition =
        match.competition || "Compétition";

    const flagEmoji =
        match.country?.emoji || "🏆";

    const scoreXpronos =
        Number(
            match.score_xpronos || 0
        ).toFixed(1);

    const bestPick =
        match.best_pick || {};

    const secondPick =
        match.second_pick || {};

    const exactScore =
        match.best_exact_score || {};

    return `

    <div class="card">

        <div class="card-header">

            <div class="rank">
                🏆 #${rank}
            </div>

            <div class="status">
                ACTIF ✅
            </div>

        </div>

        <div class="competition">

            ${flagEmoji}
            ${competition}

        </div>

        <div class="match-time">

            🗓 ${formatDate(
                match.event_date
            )}

        </div>

        <div class="teams">

            <img
                class="logo"
                src="${homeLogo}"
                alt="${match.home_team || ''}"
                loading="lazy"
            >

            <div class="vs">
                VS
            </div>

            <img
                class="logo"
                src="${awayLogo}"
                alt="${match.away_team || ''}"
                loading="lazy"
            >

        </div>

        <div class="match-name">

            ${match.home_team || '-'}

            vs

            ${match.away_team || '-'}

        </div>

        <div class="score-box">

            <div class="score-label">

                📊 Score XPRONOS

            </div>

            <div class="score-value">

                ${scoreXpronos}

            </div>

        </div>

        <div class="pick primary">

            ✅ ${bestPick.market || "-"}

            (${bestPick.confidence || 0}%)

            ${bestPick.odds
                ? `• 💰 ${bestPick.odds}`
                : ""
            }

        </div>

        <div class="pick secondary">

            ✅ ${secondPick.market || "-"}

            (${secondPick.confidence || 0}%)

            ${secondPick.odds
                ? `• 💰 ${secondPick.odds}`
                : ""
            }

        </div>

        <div class="exact">

            🎯 Score exact :

            ${exactScore.score || "-"}

        </div>

    </div>

    `;
}

function renderMatches(
    league = "all"
) {

    const container =
        document.getElementById(
            "matchesContainer"
        );

    if (!container) {
        return;
    }

    container.innerHTML = "";

    let matches =
        [...allMatches];

    if (
        league !== "all"
    ) {

        matches =
            matches.filter(
                match =>
                    match.competition === league
            );
    }

    matches.forEach(
        match => {

            container.innerHTML +=
                createCard(match);

        }
    );

    if (
        matches.length === 0
    ) {

        container.innerHTML =

        `
        <div class="card">

            Aucun match trouvé.

        </div>
        `;
    }
}

function initLeagueFilter() {

    const filter =
        document.getElementById(
            "leagueFilter"
        );

    if (!filter) {
        return;
    }

    const leagues = [

        ...new Set(

            allMatches

            .map(
                match =>
                    match.competition
            )

            .filter(
                Boolean
            )
        )
    ];

    leagues.sort();

    leagues.forEach(
        league => {

            const option =
                document.createElement(
                    "option"
                );

            option.value =
                league;

            option.textContent =
                league;

            filter.appendChild(
                option
            );
        }
    );

    filter.addEventListener(
        "change",
        () => {

            renderMatches(
                filter.value
            );

        }
    );
}

async function loadTop10() {

    try {

        const response =

            await fetch(
                "data/top10_active.json"
            );

        if (
            !response.ok
        ) {

            throw new Error(
                `HTTP ${response.status}`
            );
        }

        const data =
            await response.json();

        allMatches =
            data.matches || [];

        initLeagueFilter();

        renderMatches();

        console.log(
            `✅ ${allMatches.length} matchs chargés`
        );

    } catch (error) {

        console.error(
            "Erreur chargement Top10 :",
            error
        );

        const container =
            document.getElementById(
                "matchesContainer"
            );

        if (container) {

            container.innerHTML =

            `
            <div class="card">

                ❌ Impossible de charger
                le Top 10 XPRONOS.

            </div>
            `;
        }
    }
}

document.addEventListener(
    "DOMContentLoaded",
    loadTop10
);


        container.innerHTML =

        `
        <div class="card">

            Aucun match trouvé.

        </div>
        `;
    }
}

function initLeagueFilter() {

    const filter =
        document.getElementById(
            "leagueFilter"
        );

    if (!filter) {
        return;
    }

    const leagues = [
let allMatches = [];

function formatDate(dateString) {

    if (!dateString) {
        return "-";
    }

    const date = new Date(dateString);

    return date.toLocaleString(
        "fr-FR",
        {
            dateStyle: "medium",
            timeStyle: "short"
        }
    );
}

function createCard(match) {

    const homeLogo =
        match.home_logo || "";

    const awayLogo =
        match.away_logo || "";

    const rank =
        match.rank || "-";

    const competition =
        match.competition || "Compétition";

    const flagEmoji =
        match.country?.emoji || "🏆";

    const scoreXpronos =
        Number(
            match.score_xpronos || 0
        ).toFixed(1);

    const bestPick =
        match.best_pick || {};

    const secondPick =
        match.second_pick || {};

    const exactScore =
        match.best_exact_score || {};

    return `

    <div class="card">

        <div class="card-header">

            <div class="rank">
                🏆 #${rank}
            </div>

            <div class="status">
                ACTIF ✅
            </div>

        </div>

        <div class="competition">

            ${flagEmoji}
            ${competition}

        </div>

        <div class="match-time">

            🗓 ${formatDate(
                match.event_date
            )}

        </div>

        <div class="teams">

            <img
                class="logo"
                src="${homeLogo}"
                alt="${match.home_team || ''}"
                loading="lazy"
            >

            <div class="vs">
                VS
            </div>

            <img
                class="logo"
                src="${awayLogo}"
                alt="${match.away_team || ''}"
                loading="lazy"
            >

        </div>

        <div class="match-name">

            ${match.home_team || '-'}

            vs

            ${match.away_team || '-'}

        </div>

        <div class="score-box">

            <div class="score-label">

                📊 Score XPRONOS

            </div>

            <div class="score-value">

                ${scoreXpronos}

            </div>

        </div>

        <div class="pick primary">

            ✅ ${bestPick.market || "-"}

            (${bestPick.confidence || 0}%)

            ${bestPick.odds
                ? `• 💰 ${bestPick.odds}`
                : ""
            }

        </div>

        <div class="pick secondary">

            ✅ ${secondPick.market || "-"}

            (${secondPick.confidence || 0}%)

            ${secondPick.odds
                ? `• 💰 ${secondPick.odds}`
                : ""
            }

        </div>

        <div class="exact">

            🎯 Score exact :

            ${exactScore.score || "-"}

        </div>

    </div>

    `;
}

function renderMatches(
    league = "all"
) {

    const container =
        document.getElementById(
            "matchesContainer"
        );

    if (!container) {
        return;
    }

    container.innerHTML = "";

    let matches =
        [...allMatches];

    if (
        league !== "all"
    ) {

        matches =
            matches.filter(
                match =>
                    match.competition === league
            );
    }

    matches.forEach(
        match => {

            container.innerHTML +=
                createCard(match);

        }
    );

    if (
        matches.length === 0
    ) {

        container.innerHTML =

        `
        <div class="card">

            Aucun match trouvé.

        </div>
        `;
    }
}

function initLeagueFilter() {

    const filter =
        document.getElementById(
            "leagueFilter"
        );

    if (!filter) {
        return;
    }

    const leagues = [

        ...new Set(

            allMatches

            .map(
                match =>
                    match.competition
            )

            .filter(
                Boolean
            )
        )
    ];

    leagues.sort();

    leagues.forEach(
        league => {

            const option =
                document.createElement(
                    "option"
                );

            option.value =
                league;

            option.textContent =
                league;

            filter.appendChild(
                option
            );
        }
    );

    filter.addEventListener(
        "change",
        () => {

            renderMatches(
                filter.value
            );

        }
    );
}

async function loadTop10() {

    try {

        const response =

            await fetch(
                "data/top10_active.json"
            );

        if (
            !response.ok
        ) {

            throw new Error(
                `HTTP ${response.status}`
            );
        }

        const data =
            await response.json();

        allMatches =
            data.matches || [];

        initLeagueFilter();

        renderMatches();

        console.log(
            `✅ ${allMatches.length} matchs chargés`
        );

    } catch (error) {

        console.error(
            "Erreur chargement Top10 :",
            error
        );

        const container =
            document.getElementById(
                "matchesContainer"
            );

        if (container) {

            container.innerHTML =

            `
            <div class="card">

                ❌ Impossible de charger
                le Top 10 XPRONOS.

            </div>
            `;
        }
    }
}

document.addEventListener(
    "DOMContentLoaded",
    loadTop10
);

ption
            );
        }
    );

    filter.addEventListener(
        "change",
        () => {

            renderMatches(
                filter.value
            );

        }
    );
}

async function loadTop10() {

    try {

        const response =

            await fetch(
