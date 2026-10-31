/* GS1905 opponent and club crest system */
(()=> {
 const files={"Galatasaray":"Galatasaray_Sports_Club_Logo.svg","VfB Stuttgart":"VfB_Stuttgart_Logo.svg","Aston Villa":"Aston_Villa_FC_crest_(2016).svg","AEK Atina":"AEK_Athens_F.C._logo.svg","Feyenoord":"Feyenoord_logo.svg","Paris Saint-Germain":"Paris_Saint-Germain_F.C..svg","Fenerbahçe":"Fenerbahçe_SK_(football)_logo.svg","Barcelona":"FC_Barcelona_(crest).svg","Lille":"LOSC_Lille_logo.svg","Sporting CP":"Sporting_Clube_de_Portugal_(Logo).svg","Beşiktaş":"Beşiktaş_JK_Logo.svg","Trabzonspor":"Trabzonspor_logo.svg","Gençlerbirliği":"Gençlerbirliği_SK_logo.svg","Göztepe":"Göztepe_SK_logo.svg","Kasımpaşa":"Kasımpaşa_SK_logo.svg","Kocaelispor":"Kocaelispor_logo.svg","Konyaspor":"Konyaspor_logo.svg","Tümosan Konyaspor":"Konyaspor_logo.svg","Erzurumspor FK":"Erzurumspor_FK_logo.svg","İstanbul Başakşehir":"İstanbul_Başakşehir_FK_logo.svg","Çaykur Rizespor":"Çaykur_Rizespor_logo.svg","Samsunspor":"Samsunspor_logo.svg","Gaziantep FK":"Gaziantep_FK_logo.svg","Eyüpspor":"Eyüpspor_logo.svg","Corendon Alanyaspor":"Alanyaspor_logo.svg","Arca Çorum FK":"Çorum_FK_logo.svg","Amed Sportif Faaliyetler":"Amedspor_logo.svg","Abdülkerim Bardakcı":"Galatasaray_Sports_Club_Logo.svg","Aleksey Batrakov":"Galatasaray_Sports_Club_Logo.svg","Barış Alper Yılmaz":"Galatasaray_Sports_Club_Logo.svg","Davinson Sánchez":"Galatasaray_Sports_Club_Logo.svg","Eren Elmalı":"Galatasaray_Sports_Club_Logo.svg","Gabriel Sara":"Galatasaray_Sports_Club_Logo.svg","Ismail Jakobs":"Galatasaray_Sports_Club_Logo.svg","Leroy Sané":"Galatasaray_Sports_Club_Logo.svg","Lucas Torreira":"Galatasaray_Sports_Club_Logo.svg","Mario Lemina":"Galatasaray_Sports_Club_Logo.svg","Roland Sallai":"Galatasaray_Sports_Club_Logo.svg","Victor Osimhen":"Galatasaray_Sports_Club_Logo.svg","Yunus Akgün":"Galatasaray_Sports_Club_Logo.svg"};
 const aliases={"Konyaspor":"Tümosan Konyaspor","tümosan konyaspor":"Konyaspor","psg":"Paris Saint-Germain","fc barcelona":"Barcelona","lille osc":"Lille","gal":"Galatasaray","stu":"VfB Stuttgart","kon":"Tümosan Konyaspor","konyaspor":"Tümosan Konyaspor"};
 const clean=s=>String(s||'').trim().replace(/\s+/g,' ');
 const fileFor=name=>{const n=clean(name).toLocaleLowerCase('tr');const key=Object.keys(files).find(k=>k.toLocaleLowerCase('tr')===n);const alias=aliases[clean(name)]||aliases[n];return files[key]||files[alias]||null;};
 const initials=name=>clean(name).split(/[\s-]+/).filter(Boolean).slice(0,2).map(w=>w[0]).join('').toUpperCase();
 const fallback=(name)=>'data:image/svg+xml;charset=UTF-8,'+encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><circle cx="32" cy="32" r="29" fill="#171d3b" stroke="#f3bd28" stroke-width="2"/><text x="32" y="38" text-anchor="middle" font-family="Arial" font-size="18" font-weight="700" fill="#fff">'+initials(name)+'</text></svg>');
 const url=name=>{const f=fileFor(name);return f?'https://commons.wikimedia.org/wiki/Special:FilePath/'+encodeURIComponent(f):fallback(name)};
 const img=(name,cls='team-crest')=>'<img class="'+cls+'" src="'+url(name)+'" alt="'+clean(name)+' logosu" loading="lazy" onerror="this.onerror=null;this.src=\''+fallback(name)+'\'">';
 const decorate=()=>{
  document.querySelectorAll('.teams > span').forEach(el=>{if(el.querySelector('img'))return;const n=clean(el.textContent);el.insertAdjacentHTML('afterbegin',img(n));});
  document.querySelectorAll('.rail-teams > div').forEach(el=>{const n=clean(el.querySelector('b')?.textContent||el.textContent);let im=el.querySelector('img');if(!im){el.insertAdjacentHTML('afterbegin',img(n));im=el.querySelector('img')}im.src=url(n);im.alt=n+' logosu';im.onerror=function(){this.onerror=null;this.src=fallback(n)};});
  document.querySelectorAll('.quick-match b,.result-score span').forEach(el=>{if(el.querySelector('img'))return;const n=clean(el.textContent);el.insertAdjacentHTML('afterbegin',img(n));});
  document.querySelectorAll('.standings tbody tr td:nth-child(2),#standings tr td:nth-child(2)').forEach(el=>{if(el.querySelector('img'))return;const n=clean(el.textContent);if(n)el.insertAdjacentHTML('afterbegin',img(n));});
  document.querySelectorAll('.upcoming-row b,.rail-fixture b').forEach(el=>{
   if(el.querySelector('img'))return;
   const raw=clean(el.textContent),parts=raw.split(/\s[–—-]\s/);
   if(parts.length===2){el.innerHTML=img(parts[0])+'<span class="team-name">'+parts[0]+'</span><span class="fixture-separator">–</span>'+img(parts[1])+'<span class="team-name">'+parts[1]+'</span>';return;}
   const score=raw.match(/^(.+?)\s+(\d+\s*[:–-]\s*\d+)\s+(.+)$/);
   if(score)el.innerHTML=img(score[1])+'<span class="team-name">'+score[1]+'</span><strong class="fixture-score">'+score[2]+'</strong>'+img(score[3])+'<span class="team-name">'+score[3]+'</span>';
  });
 };
 window.GS1905TeamLogos={url,img,decorate};
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',decorate);else decorate();
 new MutationObserver(decorate).observe(document.body,{childList:true,subtree:true});
})();