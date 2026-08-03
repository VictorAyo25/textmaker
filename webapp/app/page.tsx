import { authEnabled } from '@/lib/auth';
import Providers from '@/components/Providers';
import App from '@/components/App';

// A server component purely so the client learns whether sign-in is configured
// without needing another public env var to be kept in step.
export default function Page() {
  return (
    <Providers>
      <App authEnabled={authEnabled} />
    </Providers>
  );
}
