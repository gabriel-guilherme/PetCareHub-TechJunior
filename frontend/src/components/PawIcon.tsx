import React from 'react';

export interface PawIconProps extends React.SVGProps<SVGSVGElement> {
    size?: number | string;
    color?: string;
    className: string;
}

export function PawIcon({
    size = 48,
    color = 'currentColor',
    className = '',
    ...props
}: PawIconProps) {
    return (
        <svg
      viewBox="52 202 54 50"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      width={size}
      height={size}
      className={`shrink-0 ${className}`}
      aria-hidden="true"
      {...props}
    >
      {/* Almofada esquerda superior */}
      <path
        d="M67.9966 224.837C67.9966 227.782 65.6088 230.17 62.6633 230.17C59.7178 230.17 57.33 227.782 57.33 224.837C57.33 221.891 59.7178 219.503 62.6633 219.503C65.6088 219.503 67.9966 221.891 67.9966 224.837Z"
        stroke={color}
        strokeWidth="4.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      {/* Almofada centro-esquerda */}
      <path
        d="M78.6633 211.503C78.6633 214.449 76.2754 216.837 73.3299 216.837C70.3844 216.837 67.9966 214.449 67.9966 211.503C67.9966 208.558 70.3844 206.17 73.3299 206.17C76.2754 206.17 78.6633 208.558 78.6633 211.503Z"
        stroke={color}
        strokeWidth="4.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      {/* Almofada centro-direita */}
      <path
        d="M91.9966 211.503C91.9966 214.449 89.6088 216.837 86.6633 216.837C83.7178 216.837 81.33 214.449 81.33 211.503C81.33 208.558 83.7178 206.17 86.6633 206.17C89.6088 206.17 91.9966 208.558 91.9966 211.503Z"
        stroke={color}
        strokeWidth="4.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      {/* Almofada direita superior */}
      <path
        d="M102.663 224.837C102.663 227.782 100.276 230.17 97.33 230.17C94.3845 230.17 91.9967 227.782 91.9967 224.837C91.9967 221.891 94.3845 219.503 97.33 219.503C100.276 219.503 102.663 221.891 102.663 224.837Z"
        stroke={color}
        strokeWidth="4.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      {/* Palma principal inferior */}
      <path
        d="M79.9966 228.837C71.9966 228.837 65.33 236.837 65.33 242.703C65.33 246.97 69.33 248.837 73.33 248.837C75.9966 248.837 77.5966 247.77 79.9966 247.77C82.3966 247.77 83.9966 248.837 86.6633 248.837C90.6633 248.837 94.6633 246.97 94.6633 242.703C94.6633 236.837 87.9967 228.837 79.9966 228.837Z"
        stroke={color}
        strokeWidth="4.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
    );
}