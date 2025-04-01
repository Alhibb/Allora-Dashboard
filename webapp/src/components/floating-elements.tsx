"use client"

import { useEffect, useState } from "react"
import { cn } from "@/lib/utils"

interface FloatingElement {
  id: number
  x: number
  y: number
  size: number
  speed: number
  type: "cloud" | "leaf" | "dust"
  rotation: number
  rotationSpeed: number
}

export default function FloatingElements() {
  const [elements, setElements] = useState<FloatingElement[]>([])

  useEffect(() => {
    // Create initial elements
    const newElements: FloatingElement[] = []

    // Clouds
    for (let i = 0; i < 5; i++) {
      newElements.push({
        id: i,
        x: Math.random() * 100,
        y: Math.random() * 30,
        size: 30 + Math.random() * 50,
        speed: 0.01 + Math.random() * 0.02,
        type: "cloud",
        rotation: Math.random() * 360,
        rotationSpeed: 0.01 + Math.random() * 0.05,
      })
    }

    // Leaves
    for (let i = 5; i < 15; i++) {
      newElements.push({
        id: i,
        x: Math.random() * 100,
        y: Math.random() * 100,
        size: 5 + Math.random() * 15,
        speed: 0.05 + Math.random() * 0.1,
        type: "leaf",
        rotation: Math.random() * 360,
        rotationSpeed: 0.1 + Math.random() * 0.5,
      })
    }

    // Dust sprites
    for (let i = 15; i < 30; i++) {
      newElements.push({
        id: i,
        x: Math.random() * 100,
        y: Math.random() * 100,
        size: 2 + Math.random() * 5,
        speed: 0.02 + Math.random() * 0.08,
        type: "dust",
        rotation: Math.random() * 360,
        rotationSpeed: 0.2 + Math.random() * 0.8,
      })
    }

    setElements(newElements)

    // Animation loop
    const animationInterval = setInterval(() => {
      setElements((prevElements) =>
        prevElements.map((element) => {
          let newY = element.y + element.speed
          if (newY > 110) {
            newY = -10
          }

          return {
            ...element,
            y: newY,
            rotation: (element.rotation + element.rotationSpeed) % 360,
          }
        }),
      )
    }, 50)

    return () => clearInterval(animationInterval)
  }, [])

  return (
    <div className="fixed inset-0 pointer-events-none overflow-hidden">
      {elements.map((element) => (
        <div
          key={element.id}
          className={cn(
            "absolute rounded-full opacity-70 transition-transform",
            element.type === "cloud" && "bg-white blur-md",
            element.type === "leaf" && "bg-emerald-300",
            element.type === "dust" && "bg-yellow-100",
          )}
          style={{
            left: `${element.x}%`,
            top: `${element.y}%`,
            width: `${element.size}px`,
            height: element.type === "cloud" ? `${element.size * 0.6}px` : `${element.size}px`,
            transform: `rotate(${element.rotation}deg)`,
            transition: "transform 0.5s ease-out",
          }}
        />
      ))}
    </div>
  )
}

