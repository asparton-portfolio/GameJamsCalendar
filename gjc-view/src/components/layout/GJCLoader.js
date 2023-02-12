import { Center, Loader } from '@mantine/core';

export default function GJCLoader() {
  return (
    <Center style={{
        position: 'absolute',
        top: '10.5vh',
        width: '100vw',
        height: '89.5vh',
        zIndex: 10,
        backgroundColor: 'rgba(255, 255, 255, 0.7)',
        display: 'flex',
        flexFlow: 'column nowrap'

    }}>
      <Loader size='xl' color='pink' variant= 'dots' />
      <p style={{ color: '#e64980', marginTop: '2em', fontWeight: 600 }}>
        Searching for upcoming game jams on the web...
      </p>
    </Center>
  )
}