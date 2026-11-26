const b = (color, emoji, label, headline, body) => ({ color, emoji, label, headline, body });
const svg = '<text x="270" y="1070" text-anchor="middle" class="h" font-size="17" fill="#666">.</text><rect x="0" y="0" width="10" height="10" fill="#fff"/>'.repeat(1) + Array.from({length:12},(_,i)=>`<rect x="${i}" y="0" width="1" height="1" fill="#fff"/>`).join('');
module.exports = [
  { num: 600, emoji: '🔦', title: 'Deep tech is mostly fog',
    bands: [
      b('purple', '🧩', 'What', 'Two risks open at once', ['Software asks one question: does anyone want it? Deep tech adds a second: can it be built, cheaply, in time?']),
      b('red', '🎯', 'Why it hurts', 'Plans stop working in fog', ['One hardware delay, one model release or one platform change can turn an eighteen-month roadmap into fiction by month three.']),
      b('green', '🛠️', 'How', 'Walk with a flashlight', ['# Short steps', 'Answer one question per week.', '# Leave breadcrumbs', 'Write down what each step taught you.']),
    ], svg },
  { num: 501, emoji: '🛝', title: 'Treat it like a playground',
    bands: [
      b('purple', '🧩', 'What', 'Play beats war in the fog', ['A war is rigid, burns people out and hoards the map. A playground explores, has soft edges and is shared.']),
      b('red', '🎯', 'Why it works', 'Falling is cheap and expected', ['Deep tech moves by cheap exploration, then commitment. Playgrounds are built for exactly that.']),
      b('green', '🛠️', 'How', 'Set the playground rules', ['# Fence it', 'Every experiment gets a time box and a question.', '# Enjoy it on purpose', 'Fun is the fuel that lasts a decade.']),
    ], svg },
  { num: 502, emoji: '📝', title: 'Write it that week',
    bands: [
      b('purple', '🧩', 'What', 'Lessons rot fast', ['The week after a failure you remember why it happened. A month later you remember a tidy story.']),
      b('red', '🎯', 'Why it works', 'A card is compressed context', ['One idea, small enough for a phone, ready to hand to someone who has not paid for it yet.']),
      b('green', '🛠️', 'How', 'Three parts, one screen', ['# What, why, how', 'Nothing else on the card.', '# Hand it to one person', 'A card nobody receives is a diary.']),
    ], svg },
  { num: 503, emoji: '🏮', title: 'Share context, not orders',
    bands: [
      b('purple', '🧩', 'What', 'Context is the scarce thing', ['Why we chose this. What we tried. Which demo changed a mind. Most of it lives in the founder’s head.']),
      b('red', '🎯', 'Why it works', 'Shared context compounds', ['People make the calls you would make, for your reasons, then push past you into new ground.']),
      b('green', '🛠️', 'How', 'Make sharing a ritual', ['# Starter pack', 'New people meet old mistakes on paper.', '# A card per failure', 'Written within the week, sent to all.']),
    ], svg },
  { num: 504, emoji: '🧭', title: 'Make new mistakes',
    bands: [
      b('purple', '🧩', 'What', 'Old mistakes are a tax', ['An old mistake teaches nothing new. It only costs time you will not get back.']),
      b('red', '🎯', 'Why it works', 'New mistakes are tuition', ['They mean the team is at the edge, learning something that did not exist before.']),
      b('green', '🛠️', 'How', 'Fence off the old ground', ['# Keep an archive', 'Every lesson, findable in seconds.', '# Retire what expires', 'Prune cards that stop being true.']),
    ], svg },
];
