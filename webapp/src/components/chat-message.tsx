import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { cn } from '@/lib/utils';

interface ChatMessageProps {
  message: {
    role: 'user' | 'assistant';
    content: string;
  };
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user';

  return (
    <div
      className={cn(
        'flex items-start gap-3 max-w-[80%]',
        isUser ? 'ml-auto' : 'mr-auto'
      )}
    >
      {!isUser && (
        <Avatar className='h-8 w-8 border-2 border-emerald-200'>
          <AvatarImage src='/placeholder.svg?height=32&width=32' alt='Spirit' />
          <AvatarFallback className='bg-emerald-100 text-emerald-700'>
            SP
          </AvatarFallback>
        </Avatar>
      )}

      <div
        className={cn(
          'rounded-2xl p-3 text-sm shadow-sm',
          isUser
            ? 'bg-emerald-500 text-white rounded-tr-none'
            : 'bg-white border border-emerald-100 text-gray-800 rounded-tl-none'
        )}
      >
        {message.content}
      </div>

      {isUser && (
        <Avatar className='h-8 w-8 border-2 border-emerald-200'>
          <AvatarImage src='/placeholder.svg?height=32&width=32' alt='User' />
          <AvatarFallback className='bg-emerald-500 text-white'>
            ME
          </AvatarFallback>
        </Avatar>
      )}
    </div>
  );
}
