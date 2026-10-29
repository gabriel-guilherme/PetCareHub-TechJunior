import React from 'react';

export interface CheckIconProps extends React.SVGProps<SVGSVGElement> {
    size?: number | string;
    color?: string;
    className?: string;
}

export function CheckIcon({
    size = 20,
    color = 'currentColor',
    className = '',
    ...props
}: CheckIconProps){
    return (
        <svg
            viewBox="50 400 16 13"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            width={size}
            height={size}
            className={`shrink-0 ${className}`}
            aria-hidden="true"
            {...props}
            >
            <path
                d="M52.165 406L56.3329 410.165L63.835 401.835"
                stroke={color}
                strokeWidth="2.4"
                strokeLinecap="round"
                strokeLinejoin="round"
            />
            </svg>
        );
}

export default CheckIcon;