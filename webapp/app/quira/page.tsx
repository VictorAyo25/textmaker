import type { Metadata } from 'next';
import './quira.css';
import { QUIRA_QUESTIONS } from '@/data/quira';
import Quira from '@/components/quira/Quira';

// The side quest lives on its own route with its own stylesheet, so it looks
// and behaves like the app the challenge is sat on rather than like the rest of
// this platform. Nothing here is registered in data/courses.ts, so the CU Drill
// landing page is untouched.

export const metadata: Metadata = {
  title: 'Towards Mental Exploits',
  description:
    'Practice for the Quira challenge on Towards Mental Exploits by David Oyedepo, in the app’s own question grammar and against its own clock.',
};

export default function Page() {
  return <Quira questions={QUIRA_QUESTIONS} />;
}
