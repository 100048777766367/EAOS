export function formatTimestamp(date: Date = new Date()): string {
  return date.toTimeString().split(' ')[0];
}
