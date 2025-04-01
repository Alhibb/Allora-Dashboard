'use client';

import { useState } from 'react';
import ChatMessage from '@/components/chat-message';
import FloatingElements from '@/components/floating-elements';
import { Button } from '@/components/ui/button';
import { Coins, TrendingUp, ShieldAlert, BookOpen } from 'lucide-react';

export default function Home() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content:
        "Hello! I'm your crypto spirit guide. Click one of the options below to learn about the world of cryptocurrencies.",
    },
  ]);

  const instructions = [
    {
      id: 1,
      icon: <Coins className='mr-2 h-4 w-4' />,
      label: 'What is Bitcoin?',
      response:
        'Bitcoin is like the ancient tree spirit of the crypto forest. Born in 2009 by a mysterious entity known as Satoshi Nakamoto, it was the first cryptocurrency to use blockchain technology. Like how Totoro watches over the forest, Bitcoin stands as the guardian of the crypto realm, inspiring all who came after it.',
    },
    {
      id: 2,
      icon: <TrendingUp className='mr-2 h-4 w-4' />,
      label: 'Explain blockchain',
      response:
        'Blockchain is like the river that flows through the Valley of the Wind. Each drop of water is a transaction, flowing together in blocks, creating a continuous stream of information that cannot be altered. Just as the river connects all parts of the valley, blockchain connects all transactions in a transparent, immutable ledger that anyone can see but no one can change without consensus.',
    },
    {
      id: 3,
      icon: <ShieldAlert className='mr-2 h-4 w-4' />,
      label: 'Crypto risks',
      response:
        'Like venturing into the toxic jungle in Nausicaä, the crypto world has its dangers. Market volatility can rise and fall like the winds of change. Scams lurk like toxic spores. Even the most beautiful crypto projects can hide risks. Always research thoroughly, invest only what you can afford to lose, and keep your private keys safe like Sheeta guards her crystal pendant.',
    },
    {
      id: 4,
      icon: <BookOpen className='mr-2 h-4 w-4' />,
      label: 'Getting started',
      response:
        "Beginning your crypto journey is like Chihiro entering the spirit world. First, find a reputable exchange to be your guide. Create a secure wallet to store your treasures. Start with small amounts as you learn. Read the ancient scrolls (whitepapers) before investing. And remember, like Haku helped Chihiro, the community can offer guidance when you're lost. The path may seem strange at first, but with time, you'll find your way.",
    },
  ];

  const handleInstructionClick = (instruction: any) => {
    // Add user message
    setMessages((prev) => [
      ...prev,
      {
        role: 'user',
        content: instruction.label,
      },
    ]);

    // Simulate bot response
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: instruction.response,
        },
      ]);
    }, 1000);
  };

  return (
    <main className='flex min-h-screen flex-col items-center justify-between relative overflow-hidden bg-gradient-to-b from-blue-50 to-green-50'>
      <FloatingElements />

      <div className='z-10 w-full max-w-3xl flex flex-col h-screen p-4'>
        <header className='text-center mb-6 mt-8'>
          <h1 className='text-3xl font-bold text-emerald-800 mb-2'>
            Crypto Spirit Guide
          </h1>
          <p className='text-emerald-600'>Wisdom from the digital forest</p>
        </header>

        <div className='flex-1 overflow-auto mb-4 rounded-xl bg-white/80 backdrop-blur-sm shadow-lg p-4'>
          <div className='space-y-4'>
            {messages.map((message, index) => (
              <ChatMessage key={index} message={message} />
            ))}
          </div>
        </div>

        <div className='grid grid-cols-2 gap-3 mb-8'>
          {instructions.map((instruction) => (
            <Button
              key={instruction.id}
              variant='outline'
              className='p-4 h-auto text-left flex items-center bg-white/90 border-emerald-200 hover:bg-emerald-50 hover:border-emerald-300 transition-all'
              onClick={() => handleInstructionClick(instruction)}
            >
              {instruction.icon}
              <span>{instruction.label}</span>
            </Button>
          ))}
        </div>
      </div>
    </main>
  );
}
