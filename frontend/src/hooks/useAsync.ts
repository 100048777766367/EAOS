import { useState, useCallback } from 'react';

export function useAsync<T>(asyncFn: () => Promise<T>) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const execute = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await asyncFn();
      setData(res);
    } catch (err: any) {
      setError(err.message || 'Lỗi không xác định');
    } finally {
      setLoading(false);
    }
  }, [asyncFn]);

  return { data, loading, error, execute };
}
