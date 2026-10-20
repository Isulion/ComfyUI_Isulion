# Mega Prompt V4 « Prompt Jackpot » — design

Date : 2026-10-20 · Statut : brouillon à valider

## Intention

Le Mega Prompt V3 fonctionne mais il est austère : un menu déroulant de 109 thèmes, des sélecteurs oui/non, et le prompt n'est visible qu'en branchant un autre node. L'utilisateur veut une V4 qui « brille de mille feux » : un node **coloré, animé et innovant dans toute sa manière de choisir**, pas seulement pour le thème, construit avec les techniques du skill `comfyui-supernodes` (DOM widget, widget caché sérialisé, routes, `onExecuted`, nettoyage).

Direction retenue par l'utilisateur après trois séries de maquettes : **une borne d'arcade machine à sous**. Maquette de référence (interactive) : `.superpowers/brainstorm/1944405-1792518362/content/arcade-full-v2.html`.

## Objectifs

- Un nouveau node `IsulionMegaPromptV4` (« 🕹️ Isulion Mega Prompt V4 »), catégorie `Isulion/Core`, **une seule sortie : `prompt` (STRING)**.
- Une borne d'arcade dessinée en HTML/CSS dans un DOM widget : cadre néon rose/cyan animé, enseigne « ★ PROMPT JACKPOT ★ » clignotante, écran cathodique avec lignes de balayage, levier à tirer.
- Cinq rouleaux : **Thème, Sujet, Lieu, Style, Effets**.
- **La machine tourne à chaque exécution** du workflow : les rouleaux non verrouillés sont relancés côté Python, le prompt sort, et la borne anime le résultat.
- Aperçu en direct : le levier et les autres contrôles génèrent dans le navigateur sans lancer le workflow.
- **Tous les thèmes** du registre (`THEME_HANDLERS`) sont disponibles, sans liste écrite à la main.
- Tous les champs de la V3 sont conservés sous une autre forme (voir le tableau ci-dessous).

## Non-objectifs

- Ne pas modifier ni retirer la V3 : les anciens workflows doivent continuer à marcher.
- Ne pas réécrire les 109 handlers de thème.
- Pas d'autres sorties (thème, morceaux séparés, seed) : l'utilisateur a demandé uniquement le texte.

## Anti-objectifs (échec même si « ça marche »)

- Un écran qui, **après une exécution**, n'affiche pas exactement le prompt que le node a sorti. (Avant l'exécution, ce que montre un rouleau non verrouillé n'est qu'un essai : l'utilisateur a choisi que la machine retourne à chaque exécution ; l'écran se resynchronise sur le résultat du serveur via `onExecuted`.)
- Un node qui ralentit le graphe (animations qui tournent hors écran, redessin permanent du canvas LiteGraph).
- Casser les tests de contrat existants ou décaler les `widgets_values` des workflows sauvegardés.
- Une borne illisible : le prompt complet doit toujours être lisible en entier.

## Disposition du node (validée sur maquette)

De haut en bas, dans le DOM widget :

1. **Enseigne** « ★ PROMPT JACKPOT ★ » (jaune néon, étoiles clignotantes).
2. **Écran cathodique** avec les 5 rouleaux, et à droite le **levier PULL** (boule rose, tige qui s'abaisse au clic).
3. **Panneau de contrôle** : sélecteur 3 positions **SIMPLE / DÉTAILLÉ / COMPLEXE** et champ **LoRA**.
4. **Écran PROMPT** : la sortie texte, en segments colorés (une couleur par rouleau, la LoRA en pointillés), qui s'écrit lettre par lettre avec un curseur clignotant ; actions 📋 COPIER et ✏️ ÉDITER.
5. **Derniers tirages** : **liste verticale de 5 lignes** (pas de barre de défilement horizontale — demande explicite de l'utilisateur), une par tirage, numérotée 01…05, ☆/★ favori au bout de la ligne.
6. **Pied** : numéro de tirage (`TIRAGE #042`) et graine du dernier tirage.

### Bouton d'aide « ? » (demande de l'utilisateur)

- Un petit bouton rond **« ? »** néon dans le coin supérieur droit de la borne, à côté de l'enseigne.
- Il ouvre un panneau d'aide par-dessus la borne (dans le DOM widget, style arcade, lisible : fond opaque, texte non monospace si besoin), fermé par une croix, Échap ou un clic sur « ? ».
- Contenu : à quoi sert le node, le levier et ce qui se passe à chaque exécution, chaque bouton des rouleaux (🔒 ◀ ▶ 🔍 ✏️ 👁/🚫), complexité, LoRA, écran PROMPT (clic sur un segment, copier, éditer / prompt figé), derniers tirages et favoris.
- **Bascule EN / FR** en haut du panneau. Langue par défaut : celle du navigateur (`navigator.language` commençant par `fr` → FR, sinon EN). Le choix est mémorisé par navigateur (`localStorage`, lectures/écritures dans un `try/catch`), pas dans le workflow.
- Les textes d'aide vivent dans le JS (dictionnaire `{en, fr}`), insérés en texte (pas d'`innerHTML` de contenu externe).

### Chaque rouleau

- Nom en haut, résultat au centre (icône + texte court), boutons en bas.
- **🔒/🔓** sur tous les rouleaux : un rouleau verrouillé n'est jamais relancé (ni par le levier, ni à l'exécution) et garde son texte exact.
- **Thème** : ◀ ▶ (thème précédent/suivant dans la liste triée) et 🔍 (recherche plein texte dans un panneau qui s'ouvre sur l'écran). L'icône est l'emoji qui commence déjà le `DISPLAY_NAME` du thème. **Changer de thème à la main relance immédiatement les rouleaux non verrouillés dans ce thème** (choix utilisateur « B ») et verrouille le rouleau Thème.
- Le rouleau Thème déverrouillé = thème au hasard à chaque tirage (remplace « 🎲 Dynamic Random », qui n'apparaît plus dans la liste).
- **✏️** sur Sujet et Lieu : champ de saisie **directement sur l'écran cathodique** dans le style arcade (Entrée valide, Échap annule), pas de `window.prompt`. Un rouleau avec texte perso est **épinglé** (badge ✏️, état distinct de 🔒) : voir « Décisions prises par Claude ».
- **👁/🚫** sur Lieu, Style, Effets : rouleau éteint = grisé et absent du prompt.

### Animations

- Tirage : chaque rouleau libre tourne (flou vertical), puis s'arrête l'un après l'autre (décalage ~280 ms), avec rebond et éclat jaune.
- Cadre néon qui alterne rose/cyan, enseigne clignotante, lignes de balayage qui défilent.
- Le prompt s'écrit lettre par lettre après l'arrêt du dernier rouleau.
- Toutes les animations CSS sont mises en pause (`animation-play-state: paused` via une classe) quand le node est hors écran ou l'onglet caché (IntersectionObserver + `visibilitychange`). Aucun `setDirtyCanvas` en boucle.

## Correspondance avec les champs de la V3

| V3 | V4 |
|---|---|
| `theme` (liste déroulante) | rouleau Thème (◀ ▶ 🔍 🔒) |
| « 🎲 Dynamic Random » | rouleau Thème déverrouillé |
| `custom_subject` / `custom_location` | ✏️ sur les rouleaux Sujet / Lieu |
| `include_environment` / `include_style` / `include_effects` | 👁/🚫 sur Lieu / Style / Effets |
| `lora_key` | champ LoRA, ajouté en fin de prompt |
| `complexity` | sélecteur SIMPLE / DÉTAILLÉ / COMPLEXE |
| `seed`, `randomize`, `debug_mode` | supprimés de l'interface (graine affichée, voir plus bas) |

## Fonctionnement

### État du node

Tout ce que le Python consomme est dans **un seul widget STRING caché `machine_state`** (JSON versionné, `{"version": 1, …}`), conformément au skill : masqué via `hidden` + `type="converted-widget"`, jamais `serialize:false`. Il contient au minimum :

- `theme` : nom interne + verrouillé oui/non ;
- pour chaque rouleau Sujet/Lieu/Style/Effets : texte du composant actuel, verrouillé, allumé (Lieu/Style/Effets), texte personnalisé éventuel (Sujet/Lieu) — deux drapeaux distincts : `locked` et `custom` ;
- `complexity`, `lora` ;
- le prompt figé éventuel (voir ✏️ ÉDITER).

Ce qui ne sert qu'à l'affichage va dans `node.properties` : historique (5 derniers + favoris), numéro de tirage, dernière graine.

`INPUT_TYPES` n'expose que `machine_state` (+ `unique_id` caché si utile) : la liste des thèmes **ne passe pas** par `INPUT_TYPES` (elle rendrait la fixture de contrat fragile).

### Côté Python

- Module `Core_Nodes/mega_prompt_v4.py`, qui réutilise `get_theme_registry()` de la V3 (singleton, pas de relecture des JSON).
- Une fonction pure de tirage : `(état, rouleaux à relancer, graine) → nouvel état + prompt`. Elle appelle `handler.generate(custom_subject, custom_location, include_*)` avec une graine neuve et ne remplace **que** les composants des rouleaux demandés ; les rouleaux verrouillés gardent leur texte exact.
- Assemblage du prompt : sujet, lieu, style, effets (dans cet ordre, rouleaux allumés), complément de complexité, puis LoRA ; dédoublonnage comme `deduplicate_prompt_parts` de la V3.
- `OUTPUT_NODE = True` (sinon un node non branché ne s'exécute pas).
- `generate()` à l'exécution : tire les rouleaux non verrouillés, renvoie `{"ui": {"draw": [état_résolu]}, "result": (prompt,)}`. `IS_CHANGED` renvoie `float("nan")` pour que le node soit réexécuté à chaque lancement.
- **Routes** (préfixe `/isulion/megaprompt_v4/`) :
  - `GET themes` → liste `[{name, display, icon}]` triée comme la V3 ;
  - `POST roll` → reçoit l'état + la liste des rouleaux à relancer, renvoie le nouvel état et le prompt (sert au levier, au clic sur un segment, au changement de thème).
- **Concurrence** : le RNG des handlers est partagé (`ConfigManager.random`, même objet pour tous les handlers, V3 comprise) et la route s'exécute pendant qu'un prompt peut tourner dans le thread d'exécution. Un `threading.Lock` module-level (défini à côté de `get_theme_registry()` dans `mega_prompt_V3.py`) protège tout « set_seed + generate », **dans la V4 et dans la V3** : pour la V3 c'est l'ajout d'un `with` autour de ces deux appels, sans changement de comportement ni de contrat. La route délègue le travail à `asyncio.to_thread`.
- **Tout l'assemblage du prompt** (ordre, 👁, complexité, LoRA, prompt figé) est fait côté Python ; le JS n'assemble jamais lui-même, il affiche les segments renvoyés par `roll` ou par `onExecuted` (pas de double implémentation).
- Un état absent, invalide ou d'une version inconnue retombe sur un état par défaut (thème au hasard, tout déverrouillé, tout allumé), sans exception : le node doit aussi marcher en exécution par API sans navigateur.

### Côté navigateur

- Fichier `web/mega_prompt_v4.js` (plus éventuellement un CSS injecté une fois, classes préfixées `isu-mpv4-`).
- `addDOMWidget(..., {serialize:false, hideOnZoom:false, getMinHeight})`, création dans un `requestAnimationFrame` annulable, protégée par `try/catch` (leçon du node Space Invaders).
- Après chaque modification : écriture dans `machine_state` + `callback` + `node.graph.change()` + `setDirtyCanvas`.
- `onExecuted(message)` lit `message.draw[0]`, met à jour l'état, rejoue l'animation de tirage sur le résultat du serveur et ajoute la ligne à l'historique.
- `onConfigure` recharge l'état depuis le widget restauré.
- Clavier seulement quand le champ de saisie de la borne a le focus ; molette renvoyée au graphe ; nettoyage idempotent dans `onRemoved` et `dom.onRemove`.
- Appels HTTP via `api.fetchApi`, réponses obsolètes ignorées (compteur de requêtes).

## Décisions prises par Claude (à vérifier)

- **Texte personnalisé (✏️ = épinglé, différent de 🔒)** : le texte de l'utilisateur est transmis au handler comme `custom_subject` / `custom_location` (comportement V3), et le prompt contient l'habillage du handler autour (ex. `((masterful anime rendition)) of my elf queen, ((as …))`). Un rouleau épinglé **est** relancé aux tirages : son texte perso reste, l'habillage change et suit le thème. Pour figer aussi l'habillage, on ajoute 🔒 (verrouillé = composant exact figé). Effacer le texte perso (croix dans le champ ✏️) rend le rouleau au hasard. La maquette verrouillait le rouleau à l'édition ; ce comportement est remplacé par l'épinglage pour que le sujet perso reste cohérent quand le thème change.
- **Complexité** : la V3 ne transmet jamais ce réglage aux thèmes. La V4 l'applique elle-même : SIMPLE retire les compléments de qualité, DÉTAILLÉ ajoute quelques mots de détail, COMPLEXE ajoute un bloc plus riche (composition, textures). Les listes exactes sont laissées au constructeur.
- **✏️ ÉDITER le prompt complet** : passe la borne en mode « prompt figé » (badge visible sur l'écran) : le texte édité sort tel quel à chaque exécution, et les rouleaux ne tournent plus tant qu'on n'a pas quitté ce mode (un clic sur le levier le quitte).
- **Historique** : favoris toujours affichés en tête, puis les tirages récents, 5 lignes au total ; un clic recharge l'état complet de la ligne dans la machine.
- **Icônes des rouleaux Sujet/Lieu/Style/Effets** : les textes générés n'ont pas d'emoji ; chaque rouleau garde une icône fixe par catégorie et affiche un texte court tiré du composant (les premiers mots significatifs).
- **Graine** : une graine aléatoire par tirage, affichée et gardée dans l'historique ; pas de champ seed éditable.

## Contraintes

- Python 3.10+ (voir `pyproject.toml`), aucune nouvelle dépendance.
- Imports JS : depuis `web/x.js`, `"../../scripts/app.js"` et `"../../scripts/api.js"`.
- Les fichiers de ce dépôt utilisent des fins de ligne CRLF dans certains fichiers (`__init__.py`) : les préserver.
- Mettre à jour `tests/fixtures/expected_node_keys.json`, `tests/fixtures/node_contracts_v2.json`, et ajouter le module de test à `tests/run_all.py`.

## Tests attendus

- Python : parsing de l'état (valide, absent, corrompu, version inconnue) ; un tirage ne modifie jamais un rouleau verrouillé ; même graine → même résultat ; rouleau éteint absent du prompt ; LoRA en fin de prompt ; mode prompt figé ; routes appelées avec des entrées invalides.
- JS : `node --check` + un harnais Node avec faux DOM (comme pour Space Invaders) qui crée le node, tire le levier, verrouille, change de thème, simule `onExecuted`, puis supprime le node deux fois.

## Laissé au constructeur

Structure exacte du JSON, découpage des fichiers, textes courts des rouleaux, durées précises d'animation, palette exacte (dans l'esprit de la maquette), listes de mots de complexité.
