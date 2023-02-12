import { showNotification } from '@mantine/notifications';
import { Card, Group, Image } from '@mantine/core';
import { 
  IconUsers, 
  IconAward, 
  IconAwardOff, 
  IconStar, 
  IconStarOff,
  IconCheck,
  IconX
} from '@tabler/icons'

import SaveJamButton from './SaveJamButton';

import { insertJam } from '../../services/api/jamsAPI';

export default function Jam({ jam }) {
  const onSaveClick = () => {
    insertJam(jam)
      .then(createdPageUrl =>
        showNotification({
          title: "Game Jam successfully saved in Notion's calendar",
          message: `See the created event here: ${createdPageUrl}`,
          autoClose: false,
          color: 'green',
          icon: <IconCheck size={18} />
        })
      )
      .catch(_ => 
        showNotification({
          title: "Unable to save Game Jam in Notion's calendar",
          message: 'Please, make sure your Notion IDs are valid',
          color: 'red',
          icon: <IconX size={18} />
        })
      )
  }

  return (
    <Card shadow='md' p='lg' radius='md' w='20vw' style={{
      position: 'relative'
    }}>
      <SaveJamButton onSaveClick={onSaveClick} />

      { /* Background image */ }
      {
        jam.bg_image_url && 
          <Card.Section>
            <Image
              src={jam.bg_image_url}
              height={100}
              alt={jam.name + ' background image'}
            />
          </Card.Section>
      }

      { /* Name & dates */ }
      <div style={{ 
        textAlign: 'center', 
        marginTop: '1em',
      }}>
        <h3>
            <a href={jam.url}  target='_blank' rel='noopener noreferrer'>
            {jam.name}
            </a>
        </h3>
        <h4 style={{fontWeight: 600}}>
            {new Date(jam.start_date).toLocaleDateString()} - 
            {new Date(jam.end_date).toLocaleDateString()}
        </h4>
      </div>

      { /* Participants / Ranking / Featured */ }
      <div>
        <Group>
          <IconUsers size={20} />
          <p><b>{jam.joined}</b> participants</p>
        </Group>
        <Group>
          { jam.ranked ? <IconAward size={20} /> : <IconAwardOff size={20} /> }
          <p>{ jam.ranked ? 'Ranked' : 'Not ranked' }</p>
        </Group>
        <Group>
          { jam.featured ? <IconStar size={20} /> : <IconStarOff size={20} /> }
          <p>{ jam.featured ? 'Featured' : 'Not featured' }</p>
        </Group>
      </div>
    </Card>
  )
}
