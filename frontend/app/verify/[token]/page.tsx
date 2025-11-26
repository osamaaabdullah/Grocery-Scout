'use client'
import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import Link from 'next/link'

export default function VerifyPage() {
  const { token } = useParams()
  const [message, setMessage] = useState('Verifying your account...')
  const [redirecting, setRedirecting] = useState(false)

  useEffect(() => {
    if (!token) return

    const verify = async () => {
      try {
        const res = await fetch(`/api/verify?token=${token}`)
        const data = await res.json()

        if (res.ok) {
          setMessage('Your account has been verified!')
          setRedirecting(true)
          setTimeout(() => {
            window.location.href = "/login"
          }, 10000)
        } else {
          setMessage(data.detail || 'Verification failed.')
        }

      } catch {
        setMessage('Network error. Please try again.')
      }
    }

    verify()
  }, [token])

  return (
    <div className="flex flex-col items-center mt-20 text-center">
      <h1 className="text-2xl font-bold mb-4">{message}</h1>

      {redirecting && (
        <p className="mt-2 text-sm">
          Redirecting you to login page in 10 seconds... <br />
          <Link href="/login" className="text-sky-500 underline">
            Click here if not redirected
          </Link>
        </p>
      )}
    </div>
  )
}
