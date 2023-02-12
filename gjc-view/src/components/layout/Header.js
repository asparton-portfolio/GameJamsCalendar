import { PropTypes } from 'prop-types';

import { Group, Avatar, Button } from "@mantine/core"

import gjcLogo from '../../assets/images/gjc-logo.png'

export default function Header({ onGetJamsButtonClick }) {
  return (
    <header style={{
      height: '7vh',
      padding: '1em 3em 1em 3em',
      borderBottom: '1px lightgrey',
      backgroundColor: '#fffffc',
      boxShadow: 'rgba(149, 157, 165, 0.2) 0px 8px 24px',
      display: 'flex',
      flexFlow: 'row nowrap',
      justifyContent: 'space-between',
      alignItems: 'center'
    }}>
      <Group position='left'>
        <Avatar src={gjcLogo} size='lg' />
        <h2>Game Jams Calendar</h2>
      </Group>
      <Button color='pink' onClick={_ => onGetJamsButtonClick()}>
        Search for upcoming game jams
      </Button>
    </header>
  )
}

Header.propTypes = {
  onGetJamsButtonClick: PropTypes.func
}