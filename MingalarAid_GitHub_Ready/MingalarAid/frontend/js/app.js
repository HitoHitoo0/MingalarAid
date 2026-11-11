const API = '/api';
const $ = (s, root=document) => root.querySelector(s);
const $$ = (s, root=document) => [...root.querySelectorAll(s)];
function toast(msg){const t=$('#toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),3200)}
function formMessage(form,msg,ok=true){const el=$('.form-message',form);if(el){el.textContent=msg;el.style.color=ok?'var(--primary)':'#d45b5b'}}
async function api(path,options={}){const res=await fetch(API+path,{headers:{'Content-Type':'application/json',...(options.headers||{})},credentials:'same-origin',...options});let data={};try{data=await res.json()}catch{}if(!res.ok)throw new Error(data.error||'Something went wrong');return data}
function payload(form){const data={};new FormData(form).forEach((v,k)=>{if(k==='categories'){data.categories??=[];data.categories.push(v)}else data[k]=v});return data}
$('#themeToggle').addEventListener('click',()=>{document.body.classList.toggle('dark');const on=document.body.classList.contains('dark');localStorage.setItem('mingalaraid-theme',on?'dark':'light');$('#themeToggle').textContent=on?'☀':'☾'});
if(localStorage.getItem('mingalaraid-theme')==='dark'){document.body.classList.add('dark');$('#themeToggle').textContent='☀'}
$('#menuToggle').addEventListener('click',()=>$('#mainNav').classList.toggle('open'));
$$('#mainNav a').forEach(a=>a.addEventListener('click',()=>$('#mainNav').classList.remove('open')));
$$('.amount-options button').forEach(b=>b.addEventListener('click',()=>{$$('.amount-options button').forEach(x=>x.classList.remove('selected'));b.classList.add('selected');$('#donationAmount').value=b.dataset.amount}));
$$('.auth-tabs button').forEach(b=>b.addEventListener('click',()=>{$$('.auth-tabs button').forEach(x=>x.classList.toggle('active',x===b));$('#loginForm').hidden=b.dataset.tab!=='login';$('#registerForm').hidden=b.dataset.tab!=='register'}));
async function submitForm(form,path,success){form.addEventListener('submit',async e=>{e.preventDefault();const btn=$('button[type="submit"]',form);btn.disabled=true;try{const data=await api(path,{method:'POST',body:JSON.stringify(payload(form))});formMessage(form,success(data));form.reset();if(path==='/donations/demo')formMessage(form,`Demo receipt ${data.reference_id} · ${Number(data.amount).toLocaleString()} MMK. No payment was processed.`)}catch(err){formMessage(form,err.message,false)}finally{btn.disabled=false}})}
submitForm($('#assistanceForm'),'/assistance',d=>`Your request was received. Reference ID: ${d.reference_id}. Keep your contact available.`);
submitForm($('#volunteerForm'),'/volunteers',d=>`Your volunteer application was received. Reference ID: ${d.reference_id}.`);
submitForm($('#donationForm'),'/donations/demo',d=>`Demo receipt ${d.reference_id}`);
$('#loginForm').addEventListener('submit',async e=>{e.preventDefault();try{const d=await api('/auth/login',{method:'POST',body:JSON.stringify(payload(e.currentTarget))});formMessage(e.currentTarget,`Welcome back, ${d.user.full_name}.`);updateAuth(d.user)}catch(err){formMessage(e.currentTarget,err.message,false)}});
$('#registerForm').addEventListener('submit',async e=>{e.preventDefault();try{const d=await api('/auth/register',{method:'POST',body:JSON.stringify(payload(e.currentTarget))});formMessage(e.currentTarget,'Account created successfully. You are now logged in.');updateAuth(d.user)}catch(err){formMessage(e.currentTarget,err.message,false)}});
function updateAuth(user){$('#userStatus').textContent=user?`Signed in as ${user.full_name}`:'Not signed in';$('#logoutBtn').hidden=!user}
$('#logoutBtn').addEventListener('click',async()=>{try{await api('/auth/logout',{method:'POST',body:'{}'});updateAuth(null);toast('Logged out')}catch(e){toast(e.message)}});
api('/auth/me').then(d=>updateAuth(d.user)).catch(()=>updateAuth(null));
async function loadDisasters(){try{const d=await api('/disasters');if(!d.items?.length)return;const list=$('#disasterList');list.innerHTML=d.items.map((x,i)=>`<article class="disaster-card"><div class="disaster-image flood-${['one','two','three'][i%3]}"><span>${escapeHtml(x.disaster_type)}</span></div><div class="disaster-body"><div class="meta">${escapeHtml(x.published_date)} · ${escapeHtml(x.region)}</div><h3>${escapeHtml(x.title)}</h3><p>${escapeHtml(x.description)}</p><div class="card-actions"><a href="#donation">Donate</a><a href="#volunteer">Volunteer</a></div></div></article>`).join('')}catch(e){console.info('Using built-in sample reports:',e.message)}}
function escapeHtml(s){return String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
$('#disasterSearch').addEventListener('input',filterCards);$('#regionFilter').addEventListener('change',filterCards);
function filterCards(){const q=$('#disasterSearch').value.toLowerCase(),r=$('#regionFilter').value;$$('.disaster-card').forEach(c=>{c.hidden=!(c.innerText.toLowerCase().includes(q)&&(!r||c.innerText.includes(r)))})}
loadDisasters();
