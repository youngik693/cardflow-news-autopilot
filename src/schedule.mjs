// Absolute instants keep a one-day publishing instruction from recurring tomorrow.
export function publicationSlotGate({policy, ledger=[], now=Date.now()}) {
  if (policy.publicationSlots === undefined) return {allowed:true,blocks:[],slotAt:null};
  const slots=policy.publicationSlots, minutes=policy.slotWindowMinutes;
  if (!Array.isArray(slots)||!slots.length||!Number.isFinite(minutes)||minutes<=0||minutes>30||
      slots.some(s=>typeof s!=='string'||!/(Z|[+-]\d{2}:\d{2})$/.test(s)||!Number.isFinite(Date.parse(s)))||
      new Set(slots.map(Date.parse)).size!==slots.length) {
    return {allowed:false,blocks:['PUBLICATION_SCHEDULE_INVALID'],slotAt:null};
  }
  const slotAt=slots.find(s=>now>=Date.parse(s)&&now<Date.parse(s)+minutes*60000);
  if (!slotAt) return {allowed:false,blocks:['OUTSIDE_PUBLICATION_SLOT'],slotAt:null};
  const used=ledger.some(e=>e.account===policy.targetAccount&&Date.parse(e.slotAt)===Date.parse(slotAt)&&
    ['published','publishing','needs_reconcile'].includes(e.status));
  return {allowed:!used,blocks:used?['PUBLICATION_SLOT_USED']:[],slotAt};
}

// A stable account + absolute-instant key survives retries and tomorrow's ticks.
export const publicationSlotKey=(account,slot)=>account+'|'+new Date(slot).toISOString();
export function recordSlotOutcomes(state,policy,{now=Date.now(),blockers=[]}={}) {
 state.slotOutcomes??=[];
 for(const slotAt of policy.publicationSlots||[]) {
  const key=publicationSlotKey(policy.targetAccount,slotAt),old=state.slotOutcomes.find(x=>x.key===key);
  const entries=(state.ledger||[]).filter(x=>x.account===policy.targetAccount&&Date.parse(x.slotAt)===Date.parse(slotAt));
  const published=entries.find(x=>x.status==='published'),unresolved=entries.some(x=>['publishing','needs_reconcile'].includes(x.status));
  const elapsed=now>=Date.parse(slotAt)+policy.slotWindowMinutes*60000;
  const status=published?'POSTED':unresolved?'ERROR':elapsed?'SKIPPED':'PENDING';
  const item={key,slotAt,status,checkedAt:new Date(now).toISOString(),reasons:published?[]:unresolved?['PUBLISH_RESULT_UNRESOLVED']:elapsed?[...(old?.reasons||[]),...blockers,'SLOT_WINDOW_EXPIRED']:blockers,...(published?.externalPostURL?{publicURL:published.externalPostURL}:{})};
  item.reasons=[...new Set(item.reasons)];if(old)Object.assign(old,item);else state.slotOutcomes.push(item);
 }
 return state.slotOutcomes;
}
