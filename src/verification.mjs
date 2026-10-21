import {createHash} from 'node:crypto';
// Integrity gate for a trusted, separately connected reviewer. This is not a fact checker.
const canonical=value=>Array.isArray(value)?value.map(canonical):value&&typeof value==='object'?Object.fromEntries(Object.keys(value).sort().map(k=>[k,canonical(value[k])])):value;
export const reviewPayloadHash=payload=>createHash('sha256').update(JSON.stringify(canonical(payload))).digest('hex');
const hash=s=>typeof s==='string'&&/^[a-f0-9]{64}$/.test(s);
const recent=(s,now)=>Number.isFinite(Date.parse(s))&&Date.parse(s)<=now&&now-Date.parse(s)<=10*60000;
export function validatePublicationReview({receipt,payload,now=Date.now()}){
 const blocks=[],claims=payload.assets?.claims,media=payload.assets?.mediaManifest;
 if(!receipt||receipt.verdict!=='verified'||receipt.independent!==true||!receipt.reviewerId)blocks.push('INDEPENDENT_REVIEW_REQUIRED');
 if(!recent(receipt?.reviewedAt,now))blocks.push('REVIEW_STALE');
 if(receipt?.payloadHash!==reviewPayloadHash(payload))blocks.push('FINAL_PAYLOAD_CHANGED');
 if(!Array.isArray(claims)||!claims.length||new Set(claims.map(c=>c.id)).size!==claims.length)blocks.push('FINAL_CLAIM_MANIFEST_REQUIRED');
 if(!Array.isArray(media)||media.length!==payload.assets.images.length||media.some((m,i)=>m.url!==payload.assets.images[i]||!hash(m.sha256)))blocks.push('FINAL_MEDIA_HASHES_REQUIRED');
 if(receipt?.allVisibleTextCovered!==true||receipt?.renderAuditPassed!==true)blocks.push('FINAL_RENDER_REVIEW_REQUIRED');
 const checked=receipt?.sourceChecks||[];
 if(!checked.length||checked.some(s=>!/^https:\/\//.test(s.url)||!recent(s.fetchedAt,now)||!hash(s.reviewedHash)||s.reviewedHash!==s.currentHash||s.correctionsChecked!==true))blocks.push('SOURCE_RECHECK_REQUIRED');
 for(const claim of claims||[]){
  const r=receipt?.claims?.find(c=>c.id===claim.id);
  if(!claim.text||!r||r.verdict!=='supported'||!r.sourceURLs?.length||r.sourceURLs.some(url=>!checked.some(s=>s.url===url&&s.primary===true)))blocks.push('CLAIM_UNSUPPORTED');
  if(claim.numeric&&['unit','period','population','baseline'].some(k=>typeof claim[k]!=='string'||!claim[k].trim()))blocks.push('NUMERIC_CONTEXT_MISSING');
  if(!['fact','forecast','interpretation'].includes(claim.kind)||r?.kind!==claim.kind)blocks.push('CLAIM_TYPE_UNVERIFIED');
 }
 return {allowed:blocks.length===0,blocks:[...new Set(blocks)]};
}
