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
